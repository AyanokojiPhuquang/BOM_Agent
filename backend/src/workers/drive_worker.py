"""Google Drive PDF processing worker.

Consumes tasks from Redis queue, downloads PDFs from Google Drive,
and processes them through the SAME pipeline as direct PDF upload
(pdf_to_markdown → extract_product_specs → _sync_products_from_datasheets).

PDFs are saved permanently in data/datasheets/GoogleDrive/ so they can be
downloaded later when users request datasheets for a product code.
"""

import asyncio
import json
import logging
import os
import signal
from datetime import datetime, timezone
from pathlib import Path

import httpx
from sqlmodel import select

# Import ALL models so SQLAlchemy can resolve foreign keys
import src.db.models.users  # noqa: F401
import src.db.models.conversations  # noqa: F401
import src.db.models.files  # noqa: F401
import src.db.models.products  # noqa: F401
import src.db.models.excel_refs  # noqa: F401
import src.db.models.drive_sync  # noqa: F401

from src.db.database import get_manual_db_session
from src.db.models.drive_sync import BatchJob, BatchTask
from src.services.drive.progress_notifier import ProgressNotifier
from src.services.drive.redis_client import get_redis
from src.services.drive.token_manager import TokenManager
from src.services.pdf_converter import (
    ExtractedProductSpec,
    extract_product_code_from_filename,
    extract_product_specs_from_content,
    pdf_to_markdown,
)
from src.configs import SETTINGS

logger = logging.getLogger(__name__)

# Constants
REDIS_TASK_QUEUE = "drive_sync:tasks"
REDIS_DLQ = "drive_sync:dlq"
MAX_RETRIES = 3
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
DOWNLOAD_CHUNK_SIZE = 64 * 1024  # 64KB
BACKOFF_DELAYS = [2, 4, 8]  # seconds for retries
CATEGORY = "GoogleDrive"  # Category folder name for Drive-synced files


class DriveTaskWorker:
    """Background worker that processes Google Drive PDF sync tasks.

    Uses the SAME extraction pipeline as direct PDF upload:
    1. Save PDF to data/datasheets/GoogleDrive/{folder_code}/{filename}
    2. Convert to markdown via pdfplumber
    3. Extract product specs via LLM
    4. Save to Products DB via _sync_products_from_datasheets
    """

    def __init__(self) -> None:
        self._running = True
        self._token_manager = TokenManager()
        self._notifier = ProgressNotifier()

    async def run(self) -> None:
        """Main worker loop — BRPOP from Redis queue."""
        logger.info("Drive Task Worker started. Listening on queue: %s", REDIS_TASK_QUEUE)

        redis = await get_redis()

        while self._running:
            try:
                result = await redis.brpop(REDIS_TASK_QUEUE, timeout=5)
                if result is None:
                    continue

                _, raw_payload = result
                payload = json.loads(raw_payload)
                logger.info(
                    "Picked up task %s for file %s (attempt %d)",
                    payload.get("task_id"),
                    payload.get("file_name"),
                    payload.get("attempt", 0),
                )

                try:
                    await self.process_task(payload)
                except Exception as e:
                    logger.error("Task %s failed: %s", payload.get("task_id"), str(e))
                    await self.handle_failure(payload, e)

            except asyncio.CancelledError:
                logger.info("Worker received cancellation signal.")
                break
            except TimeoutError:
                continue
            except Exception as e:
                logger.error("Unexpected error in worker loop: %s", e)
                await asyncio.sleep(5)

        logger.info("Drive Task Worker shutting down gracefully.")

    async def process_task(self, payload: dict) -> None:
        """Process a single PDF — SAME flow as datasheets upload-pdf endpoint."""
        task_id = payload["task_id"]
        batch_job_id = payload["batch_job_id"]
        user_id = payload["user_id"]
        drive_file_id = payload["drive_file_id"]
        file_name = payload["file_name"]

        # Update task status to "processing"
        async with get_manual_db_session() as session:
            stmt = select(BatchTask).where(BatchTask.id == task_id)
            result = await session.execute(stmt)
            task = result.scalars().first()
            if task:
                task.status = "processing"
                task.started_at = datetime.now(timezone.utc)
                session.add(task)

        # Get valid access token
        access_token = await self._token_manager.get_valid_token(user_id)

        # --- SAME FLOW AS UPLOAD-PDF ---
        datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()
        folder_code = extract_product_code_from_filename(file_name)
        product_dir = datasheets_dir / CATEGORY / folder_code
        product_dir.mkdir(parents=True, exist_ok=True)

        # Download PDF to permanent location (same as upload saves to disk)
        pdf_path = product_dir / file_name
        await self._download_file_streaming(access_token, drive_file_id, pdf_path)

        # Convert PDF to markdown (same as upload-pdf)
        md_path = pdf_to_markdown(pdf_path, product_dir)

        # Extract product specs via LLM (same as upload-pdf)
        md_content = md_path.read_text(encoding="utf-8")
        specs = await extract_product_specs_from_content(md_content, file_name)

        if not specs:
            specs = [ExtractedProductSpec(code=folder_code)]

        # Build product records (same format as upload-pdf)
        relative_md_path = str(md_path.relative_to(datasheets_dir))
        pdf_relative_path = str(pdf_path.relative_to(datasheets_dir))
        pdf_download_url = f"/api/datasheets/pdfs/{pdf_relative_path}"

        all_new_products = []
        for spec in specs:
            all_new_products.append({
                "code": spec.code,
                "name": spec.name or spec.code,
                "brand": spec.brand,
                "description": spec.description,
                "data_rate": spec.data_rate,
                "fiber_type": spec.fiber_type,
                "wavelength": spec.wavelength,
                "max_distance": spec.max_distance,
                "connector": spec.connector,
                "main_device": "N/A",
                "category": spec.category or CATEGORY,
                "datasheet_path": relative_md_path,
                "pdf_url": pdf_download_url,
                "raw_specs": spec.raw_specs,
            })

        # Save to DB using same function as datasheets router
        from src.app.routers.datasheets import _sync_products_from_datasheets
        created, updated = await _sync_products_from_datasheets(all_new_products)
        products_count = created + updated

        # Update task as completed
        async with get_manual_db_session() as session:
            stmt = select(BatchTask).where(BatchTask.id == task_id)
            result = await session.execute(stmt)
            task = result.scalars().first()
            if task:
                task.status = "completed"
                task.products_extracted = products_count
                task.completed_at = datetime.now(timezone.utc)
                session.add(task)

        # Update batch job counters
        async with get_manual_db_session() as session:
            stmt = select(BatchJob).where(BatchJob.id == batch_job_id)
            result = await session.execute(stmt)
            job = result.scalars().first()
            if job:
                job.completed_count += 1
                job.products_extracted += products_count
                session.add(job)

                # Notify progress
                await self._notifier.notify_task_update(
                    user_id, batch_job_id, task_id, "completed", file_name,
                    job.completed_count, job.failed_count, job.total_files,
                )

        # Check if batch is complete
        await self._check_batch_complete(batch_job_id, user_id)

        logger.info(
            "Task %s completed: %d products from %s",
            task_id, products_count, file_name,
        )

    async def handle_failure(self, payload: dict, error: Exception) -> None:
        """Retry or move to DLQ."""
        task_id = payload["task_id"]
        batch_job_id = payload["batch_job_id"]
        user_id = payload["user_id"]
        attempt = payload.get("attempt", 0)

        if attempt < MAX_RETRIES - 1:
            new_attempt = attempt + 1
            delay = BACKOFF_DELAYS[min(attempt, len(BACKOFF_DELAYS) - 1)]
            logger.info("Retrying task %s (attempt %d/%d) after %ds", task_id, new_attempt + 1, MAX_RETRIES, delay)

            await asyncio.sleep(delay)
            payload["attempt"] = new_attempt
            redis = await get_redis()
            await redis.lpush(REDIS_TASK_QUEUE, json.dumps(payload))

            async with get_manual_db_session() as session:
                stmt = select(BatchTask).where(BatchTask.id == task_id)
                result = await session.execute(stmt)
                task = result.scalars().first()
                if task:
                    task.attempt_count = new_attempt + 1
                    task.error_message = str(error)
                    task.status = "queued"
                    session.add(task)
        else:
            logger.warning("Task %s exhausted retries. Moving to DLQ.", task_id)

            dlq_entry = {
                "task_id": task_id,
                "batch_job_id": batch_job_id,
                "user_id": user_id,
                "drive_file_id": payload["drive_file_id"],
                "file_name": payload["file_name"],
                "error": str(error),
                "failed_at": datetime.now(timezone.utc).isoformat(),
            }
            redis = await get_redis()
            await redis.lpush(REDIS_DLQ, json.dumps(dlq_entry))

            async with get_manual_db_session() as session:
                stmt = select(BatchTask).where(BatchTask.id == task_id)
                result = await session.execute(stmt)
                task = result.scalars().first()
                if task:
                    task.status = "dlq"
                    task.error_message = str(error)
                    task.attempt_count = MAX_RETRIES
                    session.add(task)

            async with get_manual_db_session() as session:
                stmt = select(BatchJob).where(BatchJob.id == batch_job_id)
                result = await session.execute(stmt)
                job = result.scalars().first()
                if job:
                    job.failed_count += 1
                    session.add(job)

                    await self._notifier.notify_task_update(
                        user_id, batch_job_id, task_id, "failed", payload["file_name"],
                        job.completed_count, job.failed_count, job.total_files,
                    )

            await self._check_batch_complete(batch_job_id, user_id)

    async def _download_file_streaming(self, access_token: str, file_id: str, dest_path: Path) -> None:
        """Stream-download PDF from Google Drive to disk (64KB chunks)."""
        url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
            async with client.stream("GET", url, headers=headers) as response:
                response.raise_for_status()
                total_size = 0
                with open(dest_path, "wb") as f:
                    async for chunk in response.aiter_bytes(DOWNLOAD_CHUNK_SIZE):
                        total_size += len(chunk)
                        if total_size > MAX_FILE_SIZE:
                            f.close()
                            if dest_path.exists():
                                os.remove(dest_path)
                            raise ValueError(f"File exceeds {MAX_FILE_SIZE // (1024*1024)}MB limit")
                        f.write(chunk)

        logger.info("Downloaded %s (%d bytes) to %s", file_id, total_size, dest_path)

    async def _check_batch_complete(self, batch_job_id: str, user_id: str) -> None:
        """Mark batch as completed when all tasks are terminal."""
        async with get_manual_db_session() as session:
            stmt = select(BatchTask).where(
                BatchTask.batch_job_id == batch_job_id,
                BatchTask.status.notin_(["completed", "failed", "dlq"]),
            )
            result = await session.execute(stmt)
            pending = result.scalars().all()

            if len(pending) == 0:
                job_stmt = select(BatchJob).where(BatchJob.id == batch_job_id)
                job_result = await session.execute(job_stmt)
                job = job_result.scalars().first()
                if job and job.status != "completed":
                    job.status = "completed"
                    job.completed_at = datetime.now(timezone.utc)
                    session.add(job)
                    logger.info("Batch job %s completed.", batch_job_id)

                    await self._notifier.notify_batch_complete(
                        user_id, batch_job_id,
                        job.total_files, job.completed_count, job.failed_count,
                        job.skipped_count, job.products_extracted,
                    )


# --- Entry point ---

if __name__ == "__main__":
    worker = DriveTaskWorker()

    def shutdown(sig, frame):
        logger.info("Received signal %s, shutting down...", sig)
        worker._running = False

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    asyncio.run(worker.run())
