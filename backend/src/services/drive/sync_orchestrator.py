"""Sync Orchestrator for Google Drive batch sync jobs.

Coordinates batch job creation, task dispatch to Redis, and deduplication
of already-processed files.
"""

import json
import logging

from sqlmodel import select

from src.db.database import get_manual_db_session
from src.db.models.drive_sync import BatchJob, BatchTask
from src.services.drive.folder_scanner import FolderScanner, DriveFile
from src.services.drive.redis_client import get_redis

logger = logging.getLogger(__name__)

REDIS_TASK_QUEUE = "drive_sync:tasks"
REDIS_DLQ = "drive_sync:dlq"


class SyncOrchestrator:
    """Orchestrates batch sync jobs: scanning, deduplication, and task dispatch."""

    def __init__(self, folder_scanner: FolderScanner | None = None) -> None:
        """Initialize SyncOrchestrator.

        Args:
            folder_scanner: Optional FolderScanner instance. If not provided,
                a new one will be created.
        """
        self._folder_scanner = folder_scanner or FolderScanner()

    async def start_sync(self, user_id: str, folder_id: str) -> BatchJob:
        """Start a batch sync job for a Google Drive folder.

        Validates the folder, scans for PDFs, deduplicates against previously
        processed files, creates DB records, and enqueues tasks to Redis.

        Args:
            user_id: The user's ID.
            folder_id: The Google Drive folder ID to sync.

        Returns:
            The created BatchJob record.

        Raises:
            ValueError: If the folder is invalid or inaccessible.
            RuntimeError: If Redis is unavailable for task dispatch.
        """
        # Validate folder accessibility
        is_valid = await self._folder_scanner.validate_folder(user_id, folder_id)
        if not is_valid:
            raise ValueError(
                f"Folder {folder_id} is not accessible or does not exist."
            )

        # Scan for PDF files
        pdf_files = await self._folder_scanner.scan_folder(user_id, folder_id)

        if not pdf_files:
            # Create a completed batch job with zero files
            async with get_manual_db_session() as session:
                batch_job = BatchJob(
                    user_id=user_id,
                    folder_id=folder_id,
                    status="completed",
                    total_files=0,
                    skipped_count=0,
                )
                session.add(batch_job)
                await session.flush()
                await session.refresh(batch_job)
                return batch_job

        # Deduplicate: find files already processed successfully
        files_to_process, skipped_count = await self._deduplicate(
            user_id, pdf_files
        )

        if not files_to_process:
            # All files already processed
            async with get_manual_db_session() as session:
                batch_job = BatchJob(
                    user_id=user_id,
                    folder_id=folder_id,
                    status="completed",
                    total_files=0,
                    skipped_count=skipped_count,
                )
                session.add(batch_job)
                await session.flush()
                await session.refresh(batch_job)
                return batch_job

        # Create BatchJob and BatchTask records
        batch_job, tasks = await self._create_batch_records(
            user_id=user_id,
            folder_id=folder_id,
            files=files_to_process,
            skipped_count=skipped_count,
        )

        # Enqueue tasks to Redis
        try:
            await self._enqueue_tasks(batch_job, tasks)
        except Exception as e:
            # Mark batch job as failed if Redis is unavailable
            logger.error("Failed to enqueue tasks to Redis: %s", e)
            async with get_manual_db_session() as session:
                statement = select(BatchJob).where(BatchJob.id == batch_job.id)
                result = await session.execute(statement)
                job = result.scalars().first()
                if job:
                    job.status = "failed"
                    session.add(job)
            raise RuntimeError(
                "Failed to dispatch tasks to queue. Batch job marked as failed."
            ) from e

        return batch_job

    async def get_job_status(self, job_id: str) -> dict:
        """Get detailed status of a batch job including all tasks.

        Args:
            job_id: The batch job ID.

        Returns:
            A dict with batch job details and task list.

        Raises:
            ValueError: If the job is not found.
        """
        async with get_manual_db_session() as session:
            # Get the batch job
            statement = select(BatchJob).where(BatchJob.id == job_id)
            result = await session.execute(statement)
            batch_job = result.scalars().first()

            if not batch_job:
                raise ValueError(f"Batch job {job_id} not found.")

            # Get all tasks for this job
            tasks_statement = select(BatchTask).where(
                BatchTask.batch_job_id == job_id
            )
            tasks_result = await session.execute(tasks_statement)
            tasks = tasks_result.scalars().all()

            return {
                "job": batch_job,
                "tasks": list(tasks),
            }

    async def get_job_history(self, user_id: str) -> list[BatchJob]:
        """Get all batch jobs for a user, ordered by creation date descending.

        Args:
            user_id: The user's ID.

        Returns:
            A list of BatchJob records.
        """
        async with get_manual_db_session() as session:
            statement = (
                select(BatchJob)
                .where(BatchJob.user_id == user_id)
                .order_by(BatchJob.created_at.desc())
            )
            result = await session.execute(statement)
            jobs = result.scalars().all()
            return list(jobs)

    async def _deduplicate(
        self, user_id: str, pdf_files: list[DriveFile]
    ) -> tuple[list[DriveFile], int]:
        """Filter out files that have already been successfully processed.

        Checks the batch_tasks table for entries with matching drive_file_id
        and status 'completed'.

        Args:
            user_id: The user's ID.
            pdf_files: List of discovered PDF files.

        Returns:
            A tuple of (files to process, count of skipped files).
        """
        if not pdf_files:
            return [], 0

        drive_file_ids = [f.file_id for f in pdf_files]

        async with get_manual_db_session() as session:
            # Query for already completed file IDs
            statement = select(BatchTask.drive_file_id).where(
                BatchTask.drive_file_id.in_(drive_file_ids),
                BatchTask.status == "completed",
            )
            result = await session.execute(statement)
            completed_ids = set(result.scalars().all())

        # Filter out completed files
        files_to_process = [
            f for f in pdf_files if f.file_id not in completed_ids
        ]
        skipped_count = len(pdf_files) - len(files_to_process)

        if skipped_count > 0:
            logger.info(
                "Deduplication: skipped %d already-processed files for user %s",
                skipped_count,
                user_id,
            )

        return files_to_process, skipped_count

    async def _create_batch_records(
        self,
        user_id: str,
        folder_id: str,
        files: list[DriveFile],
        skipped_count: int,
    ) -> tuple[BatchJob, list[BatchTask]]:
        """Create BatchJob and BatchTask records in the database.

        Args:
            user_id: The user's ID.
            folder_id: The Google Drive folder ID.
            files: List of files to process (after deduplication).
            skipped_count: Number of files skipped due to deduplication.

        Returns:
            A tuple of (BatchJob, list of BatchTask records).
        """
        async with get_manual_db_session() as session:
            # Create batch job
            batch_job = BatchJob(
                user_id=user_id,
                folder_id=folder_id,
                status="processing",
                total_files=len(files),
                skipped_count=skipped_count,
            )
            session.add(batch_job)
            await session.flush()
            await session.refresh(batch_job)

            # Create batch tasks
            tasks: list[BatchTask] = []
            for file in files:
                task = BatchTask(
                    batch_job_id=batch_job.id,
                    user_id=user_id,
                    drive_file_id=file.file_id,
                    file_name=file.file_name,
                    file_size=file.file_size,
                    status="queued",
                )
                session.add(task)
                tasks.append(task)

            await session.flush()
            # Refresh tasks to get their IDs
            for task in tasks:
                await session.refresh(task)

            return batch_job, tasks

    async def _enqueue_tasks(
        self, batch_job: BatchJob, tasks: list[BatchTask]
    ) -> None:
        """Enqueue tasks to the Redis task queue.

        Args:
            batch_job: The parent batch job.
            tasks: The list of BatchTask records to enqueue.

        Raises:
            Exception: If Redis connection fails.
        """
        redis = await get_redis()

        for task in tasks:
            payload = json.dumps({
                "task_id": task.id,
                "batch_job_id": batch_job.id,
                "user_id": task.user_id,
                "drive_file_id": task.drive_file_id,
                "file_name": task.file_name,
                "file_size": task.file_size,
                "attempt": 0,
            })
            await redis.lpush(REDIS_TASK_QUEUE, payload)

        logger.info(
            "Enqueued %d tasks for batch job %s",
            len(tasks),
            batch_job.id,
        )

    async def retry_failed_tasks(self, job_id: str, user_id: str) -> dict:
        """Re-enqueue failed/DLQ tasks from a batch job back to the main queue.

        Args:
            job_id: The batch job ID.
            user_id: The user's ID (for authorization check).

        Returns:
            A dict with the count of re-enqueued tasks.

        Raises:
            ValueError: If the job is not found or doesn't belong to the user.
            RuntimeError: If Redis is unavailable.
        """
        async with get_manual_db_session() as session:
            # Verify job belongs to user
            statement = select(BatchJob).where(
                BatchJob.id == job_id,
                BatchJob.user_id == user_id,
            )
            result = await session.execute(statement)
            batch_job = result.scalars().first()

            if not batch_job:
                raise ValueError(f"Batch job {job_id} not found.")

            # Get failed/DLQ tasks
            tasks_statement = select(BatchTask).where(
                BatchTask.batch_job_id == job_id,
                BatchTask.status.in_(["failed", "dlq"]),
            )
            tasks_result = await session.execute(tasks_statement)
            failed_tasks = list(tasks_result.scalars().all())

            if not failed_tasks:
                return {"retried_count": 0}

            # Reset task statuses
            for task in failed_tasks:
                task.status = "queued"
                task.attempt_count = 0
                task.error_message = None
                session.add(task)

            # Update batch job status back to processing
            batch_job.status = "processing"
            batch_job.failed_count = max(
                0, batch_job.failed_count - len(failed_tasks)
            )
            session.add(batch_job)

        # Enqueue to Redis
        try:
            redis = await get_redis()
            for task in failed_tasks:
                payload = json.dumps({
                    "task_id": task.id,
                    "batch_job_id": batch_job.id,
                    "user_id": task.user_id,
                    "drive_file_id": task.drive_file_id,
                    "file_name": task.file_name,
                    "file_size": task.file_size,
                    "attempt": 0,
                })
                await redis.lpush(REDIS_TASK_QUEUE, payload)
        except Exception as e:
            logger.error("Failed to re-enqueue tasks to Redis: %s", e)
            raise RuntimeError(
                "Failed to re-enqueue tasks. Please try again."
            ) from e

        logger.info(
            "Re-enqueued %d failed tasks for batch job %s",
            len(failed_tasks),
            job_id,
        )

        return {"retried_count": len(failed_tasks)}
