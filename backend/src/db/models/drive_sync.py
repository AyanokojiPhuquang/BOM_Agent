"""Google Drive Sync models.

Stores OAuth tokens, batch sync jobs, and individual file processing tasks.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Text
from sqlmodel import Field, SQLModel


class DriveToken(SQLModel, table=True):
    """Stores encrypted Google OAuth tokens per user."""

    __tablename__ = "drive_tokens"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", unique=True, index=True)
    access_token: str = Field(sa_column=Column(Text, nullable=False))
    refresh_token_encrypted: str = Field(sa_column=Column(Text, nullable=False))
    token_expires_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    google_email: str | None = Field(default=None)
    folder_id: str | None = Field(default=None)
    is_connected: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )


class BatchJob(SQLModel, table=True):
    """Tracks sync batch jobs."""

    __tablename__ = "batch_jobs"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    folder_id: str
    status: str = Field(default="processing")  # processing, completed, failed
    total_files: int = Field(default=0)
    completed_count: int = Field(default=0)
    failed_count: int = Field(default=0)
    skipped_count: int = Field(default=0)
    products_extracted: int = Field(default=0)
    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    completed_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )


class BatchTask(SQLModel, table=True):
    """Individual file processing tasks within a batch."""

    __tablename__ = "batch_tasks"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    batch_job_id: str = Field(foreign_key="batch_jobs.id", index=True)
    user_id: str = Field(foreign_key="users.id")
    drive_file_id: str = Field(index=True)
    file_name: str
    file_size: int = Field(default=0)
    status: str = Field(default="queued")  # queued, processing, completed, failed, dlq
    attempt_count: int = Field(default=0)
    error_message: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    products_extracted: int = Field(default=0)
    started_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    completed_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
