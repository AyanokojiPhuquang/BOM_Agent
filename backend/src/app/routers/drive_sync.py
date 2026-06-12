"""Google Drive OAuth and Sync router.

Handles OAuth 2.0 consent flow, token exchange, disconnection, status checks,
and sync job management (start sync, job history, job status, retry failed).
"""

import logging
import secrets
from datetime import datetime, timezone
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.app.auth import get_current_user
from src.app.security import decode_token
from src.configs import SETTINGS
from src.db.models.users import User
from src.services.drive.redis_client import get_redis
from src.services.drive.sync_orchestrator import SyncOrchestrator
from src.services.drive.token_manager import TokenManager
from src.services.drive.websocket_manager import ws_manager

logger = logging.getLogger(__name__)

# Public router for the OAuth callback (no auth required — it's a redirect from Google)
public_router = APIRouter()

# Authenticated router for all other endpoints
router = APIRouter()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_REVOKE_URL = "https://oauth2.googleapis.com/revoke"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.readonly"
STATE_TTL_SECONDS = 600  # 10 minutes


def _get_token_manager() -> TokenManager:
    """Create a TokenManager instance."""
    return TokenManager()


@router.get("/drive/auth/url")
async def get_auth_url(current_user: User = Depends(get_current_user)):
    """Generate Google OAuth consent URL with CSRF state."""
    state = secrets.token_urlsafe(32)

    # Store state in Redis with user_id mapping (TTL 10 min)
    redis = await get_redis()
    await redis.set(f"oauth_state:{state}", current_user.id, ex=STATE_TTL_SECONDS)

    params = {
        "client_id": SETTINGS.google_client_id,
        "redirect_uri": SETTINGS.google_redirect_uri,
        "response_type": "code",
        "scope": OAUTH_SCOPE,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }

    url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return {"url": url}


@public_router.get("/drive/auth/callback")
async def oauth_callback(code: str | None = None, state: str | None = None, error: str | None = None):
    """Handle OAuth callback from Google.

    Validates CSRF state, exchanges code for tokens, and stores them.
    Redirects to the frontend with status indication.
    """
    frontend_base = SETTINGS.cors_origins.split(",")[0].strip()

    # Handle user-denied consent
    if error:
        return RedirectResponse(
            url=f"{frontend_base}/admin?tab=drive&status=error&reason={error}"
        )

    if not code or not state:
        return RedirectResponse(
            url=f"{frontend_base}/admin?tab=drive&status=error&reason=missing_params"
        )

    # Validate CSRF state from Redis
    redis = await get_redis()
    user_id = await redis.get(f"oauth_state:{state}")

    if not user_id:
        logger.warning("Invalid or expired OAuth state: %s", state)
        return RedirectResponse(
            url=f"{frontend_base}/admin?tab=drive&status=error&reason=invalid_state"
        )

    # Delete the state to prevent reuse
    await redis.delete(f"oauth_state:{state}")

    # Exchange authorization code for tokens
    try:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": SETTINGS.google_client_id,
                    "client_secret": SETTINGS.google_client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": SETTINGS.google_redirect_uri,
                },
            )

            if token_response.status_code != 200:
                logger.error(
                    "Token exchange failed: %s %s",
                    token_response.status_code,
                    token_response.text,
                )
                return RedirectResponse(
                    url=f"{frontend_base}/admin?tab=drive&status=error&reason=token_exchange_failed"
                )

            token_data = token_response.json()

        access_token = token_data["access_token"]
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data["expires_in"]

        if not refresh_token:
            logger.error("No refresh token in response (user may have already granted access)")
            return RedirectResponse(
                url=f"{frontend_base}/admin?tab=drive&status=error&reason=no_refresh_token"
            )

        # Get user's Google email for display
        google_email = None
        try:
            async with httpx.AsyncClient() as client:
                userinfo_response = await client.get(
                    GOOGLE_USERINFO_URL,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                if userinfo_response.status_code == 200:
                    google_email = userinfo_response.json().get("email")
        except Exception:
            logger.warning("Failed to fetch Google user info", exc_info=True)

        # Store tokens using TokenManager
        from datetime import datetime, timedelta, timezone

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        token_manager = _get_token_manager()
        await token_manager.store_tokens(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            google_email=google_email,
        )

        return RedirectResponse(
            url=f"{frontend_base}/admin?tab=drive&status=success"
        )

    except Exception:
        logger.exception("OAuth callback error")
        return RedirectResponse(
            url=f"{frontend_base}/admin?tab=drive&status=error&reason=unexpected_error"
        )


@router.post("/drive/auth/disconnect")
async def disconnect(current_user: User = Depends(get_current_user)):
    """Revoke Google tokens and delete local token records."""
    token_manager = _get_token_manager()

    # Try to get the refresh token to revoke it at Google
    from sqlmodel import select

    from src.db.database import get_manual_db_session
    from src.db.models.drive_sync import DriveToken

    try:
        async with get_manual_db_session() as session:
            statement = select(DriveToken).where(DriveToken.user_id == current_user.id)
            result = await session.execute(statement)
            token_record = result.scalars().first()

            if token_record:
                # Attempt to revoke the refresh token at Google
                refresh_token = token_manager.decrypt_token(
                    token_record.refresh_token_encrypted
                )
                try:
                    async with httpx.AsyncClient() as client:
                        await client.post(
                            GOOGLE_REVOKE_URL,
                            params={"token": refresh_token},
                            headers={
                                "Content-Type": "application/x-www-form-urlencoded"
                            },
                        )
                except Exception:
                    logger.warning(
                        "Failed to revoke Google token for user %s",
                        current_user.id,
                        exc_info=True,
                    )
    except Exception:
        logger.warning("Error during token revocation lookup", exc_info=True)

    # Always delete local tokens, even if revocation fails
    await token_manager.delete_tokens(current_user.id)

    return {"message": "Disconnected"}


@router.get("/drive/auth/status")
async def get_status(current_user: User = Depends(get_current_user)):
    """Check if user has an active Google Drive connection."""
    from sqlmodel import select

    from src.db.database import get_manual_db_session
    from src.db.models.drive_sync import DriveToken

    async with get_manual_db_session() as session:
        statement = select(DriveToken).where(
            DriveToken.user_id == current_user.id,
            DriveToken.is_connected == True,  # noqa: E712
        )
        result = await session.execute(statement)
        token_record = result.scalars().first()

    if token_record:
        return {"connected": True, "google_email": token_record.google_email}

    return {"connected": False, "google_email": None}


@router.get("/drive/folders")
async def list_drive_folders(
    parent_id: str = "root",
    current_user: User = Depends(get_current_user),
):
    """List folders in Google Drive for the user to select from.

    Args:
        parent_id: The parent folder ID to list. Defaults to 'root'.
    """
    token_manager = _get_token_manager()

    try:
        access_token = await token_manager.get_valid_token(current_user.id)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Query Google Drive for folders
    params = {
        "q": f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        "fields": "files(id,name)",
        "pageSize": 100,
        "orderBy": "name",
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/drive/v3/files",
            params=params,
            headers=headers,
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to list Google Drive folders",
            )
        data = response.json()

    folders = [{"id": f["id"], "name": f["name"]} for f in data.get("files", [])]
    return {"folders": folders, "parent_id": parent_id}


# --- Pydantic Request/Response Models for Sync Endpoints ---


class SyncStartRequest(BaseModel):
    """Request body for starting a sync job."""

    folder_id: str


class BatchTaskResponse(BaseModel):
    """Response model for a single batch task."""

    id: str
    drive_file_id: str
    file_name: str
    file_size: int
    status: str
    attempt_count: int
    error_message: str | None = None
    products_extracted: int = 0
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime


class BatchJobResponse(BaseModel):
    """Response model for a batch job."""

    id: str
    user_id: str
    folder_id: str
    status: str
    total_files: int
    completed_count: int
    failed_count: int
    skipped_count: int
    products_extracted: int
    started_at: datetime
    completed_at: datetime | None = None
    created_at: datetime


class BatchJobDetailResponse(BaseModel):
    """Response model for a batch job with task details."""

    job: BatchJobResponse
    tasks: list[BatchTaskResponse]


class SyncStartResponse(BaseModel):
    """Response model for starting a sync job."""

    job_id: str
    status: str
    total_files: int
    skipped_count: int
    message: str


class RetryResponse(BaseModel):
    """Response model for retry-failed endpoint."""

    retried_count: int
    message: str


# --- Sync Endpoints ---


def _get_sync_orchestrator() -> SyncOrchestrator:
    """Create a SyncOrchestrator instance."""
    return SyncOrchestrator()


@router.post("/drive/sync/start", response_model=SyncStartResponse)
async def start_sync(
    request: SyncStartRequest,
    current_user: User = Depends(get_current_user),
):
    """Start a batch sync job for a Google Drive folder.

    Validates the folder, scans for PDFs, deduplicates, and enqueues tasks.
    """
    orchestrator = _get_sync_orchestrator()

    try:
        batch_job = await orchestrator.start_sync(
            user_id=current_user.id,
            folder_id=request.folder_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )

    return SyncStartResponse(
        job_id=batch_job.id,
        status=batch_job.status,
        total_files=batch_job.total_files,
        skipped_count=batch_job.skipped_count,
        message=f"Sync started: {batch_job.total_files} files queued, "
        f"{batch_job.skipped_count} skipped (already processed).",
    )


@router.get("/drive/sync/jobs", response_model=list[BatchJobResponse])
async def get_jobs(current_user: User = Depends(get_current_user)):
    """Get the user's sync job history."""
    orchestrator = _get_sync_orchestrator()
    jobs = await orchestrator.get_job_history(user_id=current_user.id)

    return [
        BatchJobResponse(
            id=job.id,
            user_id=job.user_id,
            folder_id=job.folder_id,
            status=job.status,
            total_files=job.total_files,
            completed_count=job.completed_count,
            failed_count=job.failed_count,
            skipped_count=job.skipped_count,
            products_extracted=job.products_extracted,
            started_at=job.started_at,
            completed_at=job.completed_at,
            created_at=job.created_at,
        )
        for job in jobs
    ]


@router.get("/drive/sync/jobs/{job_id}", response_model=BatchJobDetailResponse)
async def get_job_detail(
    job_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get detailed status of a specific batch job including all tasks."""
    orchestrator = _get_sync_orchestrator()

    try:
        result = await orchestrator.get_job_status(job_id=job_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    job = result["job"]

    # Verify the job belongs to the current user
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch job not found.",
        )

    tasks = result["tasks"]

    return BatchJobDetailResponse(
        job=BatchJobResponse(
            id=job.id,
            user_id=job.user_id,
            folder_id=job.folder_id,
            status=job.status,
            total_files=job.total_files,
            completed_count=job.completed_count,
            failed_count=job.failed_count,
            skipped_count=job.skipped_count,
            products_extracted=job.products_extracted,
            started_at=job.started_at,
            completed_at=job.completed_at,
            created_at=job.created_at,
        ),
        tasks=[
            BatchTaskResponse(
                id=task.id,
                drive_file_id=task.drive_file_id,
                file_name=task.file_name,
                file_size=task.file_size,
                status=task.status,
                attempt_count=task.attempt_count,
                error_message=task.error_message,
                products_extracted=task.products_extracted,
                started_at=task.started_at,
                completed_at=task.completed_at,
                created_at=task.created_at,
            )
            for task in tasks
        ],
    )


@router.post(
    "/drive/sync/jobs/{job_id}/retry-failed", response_model=RetryResponse
)
async def retry_failed(
    job_id: str,
    current_user: User = Depends(get_current_user),
):
    """Re-enqueue failed/DLQ tasks from a batch job back to the main queue."""
    orchestrator = _get_sync_orchestrator()

    try:
        result = await orchestrator.retry_failed_tasks(
            job_id=job_id,
            user_id=current_user.id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )

    return RetryResponse(
        retried_count=result["retried_count"],
        message=f"Re-enqueued {result['retried_count']} failed tasks.",
    )


# --- WebSocket Endpoint ---


@public_router.websocket("/drive/ws")
async def drive_websocket(websocket: WebSocket, token: str = ""):
    """WebSocket for real-time sync progress updates.

    Authentication is performed via JWT token passed as query parameter
    (?token=...) since WebSocket connections cannot use Authorization headers.
    """
    # Authenticate via JWT token in query param
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            await websocket.close(code=4001)
            return
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=4001)
            return
    except Exception:
        await websocket.close(code=4001)
        return

    await websocket.accept()
    await ws_manager.register(user_id, websocket)

    try:
        while True:
            # Keep connection alive — client may send pings or keepalives
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await ws_manager.unregister(user_id)
