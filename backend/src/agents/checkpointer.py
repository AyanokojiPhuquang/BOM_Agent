"""Checkpointer singleton for LangGraph conversation persistence.

Uses async PostgreSQL checkpointer with a connection pool
for concurrent request support.
"""

from typing import Optional

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from loguru import logger
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from src.configs import SETTINGS

_checkpointer: AsyncPostgresSaver | None = None
_connection_pool: AsyncConnectionPool | None = None

DEFAULT_POOL_SIZE = 5
CONNECTION_TIMEOUT = 5


async def get_checkpointer() -> Optional[AsyncPostgresSaver]:
    """Return the shared AsyncPostgresSaver instance, creating it on first call.

    Uses a psycopg AsyncConnectionPool instead of a single connection
    to support concurrent requests without "another command is already in progress" errors.
    """
    global _checkpointer, _connection_pool
    if _checkpointer is not None:
        return _checkpointer

    try:
        _connection_pool = AsyncConnectionPool(
            SETTINGS.checkpoint_db_url,
            open=False,
            max_size=DEFAULT_POOL_SIZE,
            kwargs={
                "autocommit": True,
                "connect_timeout": CONNECTION_TIMEOUT,
                "prepare_threshold": None,
                "row_factory": dict_row,
            },
        )
        await _connection_pool.open()

        _checkpointer = AsyncPostgresSaver(conn=_connection_pool)
        _checkpointer.supports_pipeline = False
        await _checkpointer.setup()

        logger.info(
            f"PostgreSQL checkpointer initialized (pool_size: {DEFAULT_POOL_SIZE})"
        )
        return _checkpointer

    except Exception as e:
        if _connection_pool:
            try:
                await _connection_pool.close()
            except Exception as close_error:
                logger.warning(f"Error closing connection pool: {close_error}")
            _connection_pool = None

        logger.warning(
            f"Failed to initialize checkpointer: {e}. Proceeding without persistence."
        )
        return None
