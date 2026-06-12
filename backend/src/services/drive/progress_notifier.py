"""Progress Notifier — publishes events to Redis Pub/Sub.

Worker processes call this to emit progress events. Each FastAPI server
subscribes via WebSocketManager and forwards to locally-connected clients.
"""

import json
import logging

from src.services.drive.redis_client import get_redis

logger = logging.getLogger(__name__)

CHANNEL_PREFIX = "drive_sync:progress:"


class ProgressNotifier:
    """Publishes sync progress events to Redis Pub/Sub channels."""

    async def publish(self, user_id: str, event: dict) -> None:
        """Serialize event to JSON and publish to the user's channel.

        Args:
            user_id: The target user's ID.
            event: The event payload dict to publish.
        """
        redis = await get_redis()
        channel = f"{CHANNEL_PREFIX}{user_id}"
        await redis.publish(channel, json.dumps(event))

    async def notify_task_update(
        self,
        user_id: str,
        batch_job_id: str,
        task_id: str,
        status: str,
        file_name: str,
        completed: int,
        failed: int,
        total: int,
    ) -> None:
        """Emit a task status update event.

        Args:
            user_id: The user who owns the batch job.
            batch_job_id: The batch job ID.
            task_id: The individual task ID.
            status: New task status (processing, completed, failed).
            file_name: Name of the file being processed.
            completed: Number of completed tasks in the batch.
            failed: Number of failed tasks in the batch.
            total: Total number of tasks in the batch.
        """
        await self.publish(user_id, {
            "type": "task_update",
            "batch_job_id": batch_job_id,
            "task_id": task_id,
            "status": status,
            "file_name": file_name,
            "progress": {
                "completed": completed,
                "failed": failed,
                "total": total,
            },
        })

    async def notify_batch_complete(
        self,
        user_id: str,
        batch_job_id: str,
        total_files: int,
        completed: int,
        failed: int,
        skipped: int,
        products_extracted: int,
    ) -> None:
        """Emit a batch completion event with summary.

        Args:
            user_id: The user who owns the batch job.
            batch_job_id: The batch job ID.
            total_files: Total files in the batch.
            completed: Successfully completed count.
            failed: Failed/DLQ count.
            skipped: Skipped (deduplicated) count.
            products_extracted: Total products extracted.
        """
        await self.publish(user_id, {
            "type": "batch_complete",
            "batch_job_id": batch_job_id,
            "summary": {
                "total_files": total_files,
                "completed": completed,
                "failed": failed,
                "skipped": skipped,
                "products_extracted": products_extracted,
            },
        })
