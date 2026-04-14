"""One-time migration script: SQLite -> PostgreSQL.

Usage:
    cd backend
    python -m scripts.migrate_sqlite_to_postgres

Requires:
    - PostgreSQL running and accessible (tables already created via app startup or alembic)
    - The old starlink.db file present at SQLITE_PATH

The script reads all rows from each SQLite table and bulk-inserts them
into PostgreSQL, preserving primary keys and all data. Tables are
migrated in foreign-key order to avoid constraint violations.
"""

import asyncio
import json
import os
import sqlite3
from datetime import datetime, timezone

import asyncpg

# --- Configuration ---
SQLITE_PATH = os.environ.get("SQLITE_PATH", "starlink.db")
POSTGRES_URL = os.environ.get(
    "POSTGRES_URL",
    os.environ.get("CHECKPOINT_DB_URL", "postgresql://starlink:starlink@localhost:5437/starlink"),
)

# Tables in insertion order (respecting foreign keys)
TABLES = [
    "users",
    "nhanh_tokens",
    "nhanh_sync_logs",
    "nhanh_products",
    "conversations",
    "conversation_messages",
]


def read_sqlite_table(conn: sqlite3.Connection, table: str) -> tuple[list[str], list[tuple]]:
    """Return (column_names, rows) for a table."""
    cur = conn.execute(f'SELECT * FROM "{table}"')
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return columns, rows


def parse_datetime(val) -> datetime | None:
    """Parse SQLite datetime string to timezone-aware Python datetime."""
    if val is None:
        return None
    if isinstance(val, datetime):
        if val.tzinfo is None:
            return val.replace(tzinfo=timezone.utc)
        return val
    if not isinstance(val, str):
        return val
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(val, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime: {val!r}")


def convert_value(val, col_name: str, table: str):
    """Convert a SQLite value to a PostgreSQL-compatible value."""
    if val is None:
        return None
    # Boolean columns
    if col_name == "is_active":
        return bool(val)
    # Datetime columns
    if col_name in ("created_at", "updated_at", "started_at", "finished_at", "last_synced_at"):
        return parse_datetime(val)
    # JSON columns
    if col_name == "images":
        if isinstance(val, str):
            try:
                return json.dumps(json.loads(val))
            except (json.JSONDecodeError, TypeError):
                return val
        return json.dumps(val) if val is not None else None
    return val


async def migrate():
    # Read from SQLite
    sqlite_conn = sqlite3.connect(SQLITE_PATH)

    # Connect to PostgreSQL
    pg_conn = await asyncpg.connect(POSTGRES_URL)

    try:
        for table in TABLES:
            columns, rows = read_sqlite_table(sqlite_conn, table)
            if not rows:
                print(f"  {table}: 0 rows (skipped)")
                continue

            # Convert values
            converted_rows = []
            for row in rows:
                converted = tuple(
                    convert_value(val, col, table)
                    for val, col in zip(row, columns)
                )
                converted_rows.append(converted)

            # Build INSERT ... ON CONFLICT DO NOTHING to handle re-runs
            placeholders = ", ".join(f"${i+1}" for i in range(len(columns)))
            col_list = ", ".join(f'"{c}"' for c in columns)
            query = f'INSERT INTO "{table}" ({col_list}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'

            # Bulk insert
            await pg_conn.executemany(query, converted_rows)
            print(f"  {table}: {len(converted_rows)} rows migrated")

    finally:
        await pg_conn.close()
        sqlite_conn.close()

    print("\nMigration complete!")


if __name__ == "__main__":
    print("Migrating data from SQLite to PostgreSQL...\n")
    asyncio.run(migrate())
