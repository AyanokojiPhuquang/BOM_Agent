"""Folder Scanner for Google Drive PDF discovery.

Recursively scans a Google Drive folder to discover all PDF files,
handling pagination and rate-limiting with exponential backoff.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Callable

import httpx

from src.services.drive.token_manager import TokenManager

logger = logging.getLogger(__name__)

DRIVE_API_BASE = "https://www.googleapis.com/drive/v3/files"
MAX_RETRIES = 5
BACKOFF_BASE_SECONDS = 1


@dataclass
class DriveFile:
    """Represents a PDF file discovered in Google Drive."""

    file_id: str
    file_name: str
    file_size: int


class FolderScanner:
    """Recursively discovers PDF files in a Google Drive folder.

    Uses Google Drive API v3 with pagination and exponential backoff
    on rate-limit errors (403/429).
    """

    def __init__(self, token_manager: TokenManager | None = None) -> None:
        """Initialize FolderScanner.

        Args:
            token_manager: Optional TokenManager instance. If not provided,
                a new one will be created.
        """
        self._token_manager = token_manager or TokenManager()

    async def validate_folder(self, user_id: str, folder_id: str) -> bool:
        """Check if a folder exists and is accessible via the user's credentials.

        Args:
            user_id: The user's ID for token retrieval.
            folder_id: The Google Drive folder ID to validate.

        Returns:
            True if the folder exists and is accessible, False otherwise.
        """
        try:
            access_token = await self._token_manager.get_valid_token(user_id)
        except (ValueError, RuntimeError) as e:
            logger.error("Failed to get token for user %s: %s", user_id, e)
            return False

        url = f"{DRIVE_API_BASE}/{folder_id}"
        params = {"fields": "id,name,mimeType"}
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    return True
                logger.warning(
                    "Folder validation failed for %s: %s %s",
                    folder_id,
                    response.status_code,
                    response.text,
                )
                return False
            except httpx.HTTPError as e:
                logger.error("HTTP error validating folder %s: %s", folder_id, e)
                return False

    async def scan_folder(
        self,
        user_id: str,
        folder_id: str,
        on_progress: Callable[[int], None] | None = None,
    ) -> list[DriveFile]:
        """Recursively scan a Google Drive folder for PDF files.

        Discovers all files with MIME type 'application/pdf' in the given
        folder and all nested subfolders using paginated API requests.

        Args:
            user_id: The user's ID for token retrieval.
            folder_id: The Google Drive folder ID to scan.
            on_progress: Optional callback invoked with the current count
                of discovered PDF files.

        Returns:
            A list of DriveFile objects representing all PDFs found.

        Raises:
            ValueError: If no token record exists for the user.
            RuntimeError: If token refresh fails or API errors exhaust retries.
        """
        access_token = await self._token_manager.get_valid_token(user_id)
        results: list[DriveFile] = []

        await self._scan_folder_recursive(
            access_token=access_token,
            folder_id=folder_id,
            results=results,
            on_progress=on_progress,
        )

        return results

    async def _scan_folder_recursive(
        self,
        access_token: str,
        folder_id: str,
        results: list[DriveFile],
        on_progress: Callable[[int], None] | None = None,
    ) -> None:
        """Recursively scan a folder, collecting PDFs and descending into subfolders.

        Args:
            access_token: A valid Google API access token.
            folder_id: The folder ID to list.
            results: Accumulator list for discovered PDF files.
            on_progress: Optional progress callback.
        """
        page_token: str | None = None

        while True:
            items, next_page_token = await self._list_folder_page(
                access_token=access_token,
                folder_id=folder_id,
                page_token=page_token,
            )

            subfolder_ids: list[str] = []

            for item in items:
                mime_type = item.get("mimeType", "")
                if mime_type == "application/vnd.google-apps.folder":
                    subfolder_ids.append(item["id"])
                elif mime_type == "application/pdf":
                    drive_file = DriveFile(
                        file_id=item["id"],
                        file_name=item.get("name", ""),
                        file_size=int(item.get("size", 0)),
                    )
                    results.append(drive_file)
                    if on_progress:
                        on_progress(len(results))

            # Recurse into subfolders
            for subfolder_id in subfolder_ids:
                await self._scan_folder_recursive(
                    access_token=access_token,
                    folder_id=subfolder_id,
                    results=results,
                    on_progress=on_progress,
                )

            # Handle pagination
            if next_page_token:
                page_token = next_page_token
            else:
                break

    async def _list_folder_page(
        self,
        access_token: str,
        folder_id: str,
        page_token: str | None = None,
    ) -> tuple[list[dict], str | None]:
        """List one page of files in a folder with retry and backoff.

        Args:
            access_token: A valid Google API access token.
            folder_id: The folder to list.
            page_token: Optional page token for continuation.

        Returns:
            A tuple of (list of file metadata dicts, next page token or None).

        Raises:
            RuntimeError: If the request fails after MAX_RETRIES attempts.
        """
        params: dict = {
            "q": f"'{folder_id}' in parents and trashed = false",
            "fields": "nextPageToken, files(id, name, mimeType, size)",
            "pageSize": 1000,
        }
        if page_token:
            params["pageToken"] = page_token

        headers = {"Authorization": f"Bearer {access_token}"}

        for attempt in range(MAX_RETRIES + 1):
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(
                        DRIVE_API_BASE,
                        params=params,
                        headers=headers,
                    )

                    if response.status_code == 200:
                        data = response.json()
                        files = data.get("files", [])
                        next_token = data.get("nextPageToken")
                        return files, next_token

                    if response.status_code in (403, 429):
                        if attempt < MAX_RETRIES:
                            wait_time = BACKOFF_BASE_SECONDS * (2**attempt)
                            logger.warning(
                                "Rate limited (HTTP %s) on folder %s, "
                                "retrying in %ss (attempt %d/%d)",
                                response.status_code,
                                folder_id,
                                wait_time,
                                attempt + 1,
                                MAX_RETRIES,
                            )
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            raise RuntimeError(
                                f"Google Drive API rate limit exceeded after "
                                f"{MAX_RETRIES} retries for folder {folder_id}"
                            )

                    # Other non-success status codes
                    raise RuntimeError(
                        f"Google Drive API error: {response.status_code} "
                        f"{response.text}"
                    )

                except httpx.HTTPError as e:
                    if attempt < MAX_RETRIES:
                        wait_time = BACKOFF_BASE_SECONDS * (2**attempt)
                        logger.warning(
                            "HTTP error listing folder %s: %s, "
                            "retrying in %ss (attempt %d/%d)",
                            folder_id,
                            e,
                            wait_time,
                            attempt + 1,
                            MAX_RETRIES,
                        )
                        await asyncio.sleep(wait_time)
                        continue
                    raise RuntimeError(
                        f"Failed to list folder {folder_id} after "
                        f"{MAX_RETRIES} retries: {e}"
                    ) from e

        # Should not reach here, but satisfy type checker
        raise RuntimeError(f"Failed to list folder {folder_id}")
