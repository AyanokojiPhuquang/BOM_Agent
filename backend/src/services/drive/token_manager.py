"""Token Manager for Google Drive OAuth tokens.

Handles encrypted storage, retrieval, refresh, and lifecycle management
of Google OAuth 2.0 tokens using Fernet symmetric encryption.
"""

import logging
from datetime import datetime, timedelta, timezone

import httpx
from cryptography.fernet import Fernet
from sqlmodel import select

from src.configs import SETTINGS
from src.db.database import get_manual_db_session
from src.db.models.drive_sync import DriveToken

logger = logging.getLogger(__name__)


class TokenManager:
    """Manages encrypted Google OAuth token storage and refresh."""

    TOKEN_EXPIRY_BUFFER = timedelta(minutes=5)
    GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

    def __init__(self) -> None:
        """Initialize TokenManager with encryption key from settings.

        Raises:
            ValueError: If TOKEN_ENCRYPTION_KEY is not configured.
        """
        if not SETTINGS.token_encryption_key:
            raise ValueError(
                "TOKEN_ENCRYPTION_KEY is not configured. "
                "Generate one with: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
            )
        self._fernet = Fernet(SETTINGS.token_encryption_key.encode())

    def encrypt_token(self, plaintext: str) -> str:
        """Encrypt a token string using Fernet symmetric encryption.

        Args:
            plaintext: The token string to encrypt.

        Returns:
            The encrypted token as a string.
        """
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt_token(self, ciphertext: str) -> str:
        """Decrypt a token string using Fernet symmetric encryption.

        Args:
            ciphertext: The encrypted token string.

        Returns:
            The decrypted plaintext token.
        """
        return self._fernet.decrypt(ciphertext.encode()).decode()

    async def store_tokens(
        self,
        user_id: str,
        access_token: str,
        refresh_token: str,
        expires_at: datetime,
        google_email: str | None = None,
    ) -> None:
        """Store OAuth tokens for a user, encrypting the refresh token.

        If a record already exists for the user, it will be updated.

        Args:
            user_id: The user's ID.
            access_token: The Google access token (stored in plain text).
            refresh_token: The Google refresh token (will be encrypted).
            expires_at: When the access token expires.
            google_email: Optional Google email associated with the account.
        """
        encrypted_refresh = self.encrypt_token(refresh_token)

        async with get_manual_db_session() as session:
            statement = select(DriveToken).where(DriveToken.user_id == user_id)
            result = await session.execute(statement)
            existing = result.scalars().first()

            if existing:
                existing.access_token = access_token
                existing.refresh_token_encrypted = encrypted_refresh
                existing.token_expires_at = expires_at
                existing.is_connected = True
                existing.updated_at = datetime.now(timezone.utc)
                if google_email is not None:
                    existing.google_email = google_email
                session.add(existing)
            else:
                token_record = DriveToken(
                    user_id=user_id,
                    access_token=access_token,
                    refresh_token_encrypted=encrypted_refresh,
                    token_expires_at=expires_at,
                    google_email=google_email,
                    is_connected=True,
                )
                session.add(token_record)

    async def get_valid_token(self, user_id: str) -> str:
        """Get a valid access token for a user, refreshing if needed.

        Checks if the token expires within the 5-minute buffer. If so,
        refreshes using Google's token endpoint and updates the DB record.

        Args:
            user_id: The user's ID.

        Returns:
            A valid access token string.

        Raises:
            ValueError: If no token record exists for the user.
            RuntimeError: If token refresh fails.
        """
        async with get_manual_db_session() as session:
            statement = select(DriveToken).where(DriveToken.user_id == user_id)
            result = await session.execute(statement)
            token_record = result.scalars().first()

            if not token_record:
                raise ValueError(f"No token record found for user {user_id}")

            # Check if token is still valid (not within expiry buffer)
            now = datetime.now(timezone.utc)
            expires_at = token_record.token_expires_at
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)

            if expires_at > now + self.TOKEN_EXPIRY_BUFFER:
                return token_record.access_token

            # Token is expired or within buffer — refresh it
            refresh_token = self.decrypt_token(token_record.refresh_token_encrypted)
            new_access_token, new_expires_at = await self._refresh_access_token(
                refresh_token
            )

            # Update the DB record
            token_record.access_token = new_access_token
            token_record.token_expires_at = new_expires_at
            token_record.updated_at = datetime.now(timezone.utc)
            session.add(token_record)

            return new_access_token

    async def _refresh_access_token(
        self, refresh_token: str
    ) -> tuple[str, datetime]:
        """Refresh the access token using Google's token endpoint.

        Args:
            refresh_token: The decrypted refresh token.

        Returns:
            Tuple of (new_access_token, new_expires_at).

        Raises:
            RuntimeError: If the refresh request fails.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.GOOGLE_TOKEN_ENDPOINT,
                data={
                    "client_id": SETTINGS.google_client_id,
                    "client_secret": SETTINGS.google_client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
            )

            if response.status_code != 200:
                logger.error(
                    "Token refresh failed: %s %s",
                    response.status_code,
                    response.text,
                )
                raise RuntimeError(
                    f"Failed to refresh Google token: {response.status_code}"
                )

            data = response.json()
            new_access_token = data["access_token"]
            expires_in = data["expires_in"]
            new_expires_at = datetime.now(timezone.utc) + timedelta(
                seconds=expires_in
            )

            return new_access_token, new_expires_at

    async def delete_tokens(self, user_id: str) -> None:
        """Delete all token records for a user.

        Args:
            user_id: The user's ID.
        """
        async with get_manual_db_session() as session:
            statement = select(DriveToken).where(DriveToken.user_id == user_id)
            result = await session.execute(statement)
            token_record = result.scalars().first()

            if token_record:
                await session.delete(token_record)

    async def is_connected(self, user_id: str) -> bool:
        """Check if a user has an active Google Drive connection.

        Args:
            user_id: The user's ID.

        Returns:
            True if the user has a token record with is_connected=True.
        """
        async with get_manual_db_session() as session:
            statement = select(DriveToken).where(
                DriveToken.user_id == user_id,
                DriveToken.is_connected == True,  # noqa: E712
            )
            result = await session.execute(statement)
            token_record = result.scalars().first()
            return token_record is not None

    async def mark_disconnected(self, user_id: str) -> None:
        """Mark a user's Google Drive connection as disconnected.

        Used when the refresh token is revoked or invalid.

        Args:
            user_id: The user's ID.
        """
        async with get_manual_db_session() as session:
            statement = select(DriveToken).where(DriveToken.user_id == user_id)
            result = await session.execute(statement)
            token_record = result.scalars().first()

            if token_record:
                token_record.is_connected = False
                token_record.updated_at = datetime.now(timezone.utc)
                session.add(token_record)
