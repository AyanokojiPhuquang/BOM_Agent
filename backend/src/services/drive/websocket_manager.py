"""WebSocket Manager — subscribes to Redis Pub/Sub and forwards to connected clients.

Each FastAPI process runs one WebSocketManager instance that:
1. Maintains a map of user_id -> WebSocket connections for THIS process.
2. Listens on Redis Pub/Sub pattern `drive_sync:progress:*`.
3. Routes incoming messages to the correct local WebSocket client.

This ensures progress events from the worker reach the right user regardless
of which FastAPI process holds their WebSocket connection.
"""

import asyncio
import logging

import redis.asyncio as aioredis
from fastapi import WebSocket

from src.configs import SETTINGS

logger = logging.getLogger(__name__)

CHANNEL_PATTERN = "drive_sync:progress:*"


class WebSocketManager:
    """Manages WebSocket connections and Redis Pub/Sub forwarding."""

    def __init__(self) -> None:
        """Initialize the manager with empty connection registry."""
        self._connections: dict[str, WebSocket] = {}  # user_id -> websocket
        self._listener_task: asyncio.Task | None = None

    async def register(self, user_id: str, websocket: WebSocket) -> None:
        """Register a WebSocket connection for a user.

        Args:
            user_id: The authenticated user's ID.
            websocket: The WebSocket instance to register.
        """
        self._connections[user_id] = websocket
        logger.debug("WebSocket registered for user %s", user_id)

    async def unregister(self, user_id: str) -> None:
        """Remove a user's WebSocket connection.

        Args:
            user_id: The user to unregister.
        """
        self._connections.pop(user_id, None)
        logger.debug("WebSocket unregistered for user %s", user_id)

    async def start_listener(self) -> None:
        """Start the background task that subscribes to Redis Pub/Sub."""
        self._listener_task = asyncio.create_task(self._listen())
        logger.info("WebSocket Redis listener started.")

    async def stop_listener(self) -> None:
        """Stop the background Redis listener task."""
        if self._listener_task:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass
            self._listener_task = None
            logger.info("WebSocket Redis listener stopped.")

    async def _listen(self) -> None:
        """Subscribe to Redis Pub/Sub and forward messages to local WebSocket clients."""
        redis_client = aioredis.from_url(SETTINGS.redis_url, decode_responses=True)
        pubsub = redis_client.pubsub()
        await pubsub.psubscribe(CHANNEL_PATTERN)

        try:
            async for message in pubsub.listen():
                if message["type"] != "pmessage":
                    continue

                # Channel format: drive_sync:progress:{user_id}
                channel: str = message["channel"]
                user_id = channel.split(":")[-1]
                ws = self._connections.get(user_id)

                if ws:
                    try:
                        await ws.send_text(message["data"])
                    except Exception:
                        # Connection likely closed — clean up
                        logger.debug(
                            "Failed to send to WebSocket for user %s, removing.",
                            user_id,
                        )
                        await self.unregister(user_id)
        except asyncio.CancelledError:
            pass
        finally:
            await pubsub.unsubscribe()
            await redis_client.aclose()


# Singleton instance shared across the FastAPI process
ws_manager = WebSocketManager()
