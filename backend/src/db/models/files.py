import uuid
from datetime import datetime, timezone

from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


class Folder(SQLModel, table=True):
    __tablename__ = "folders"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    parent_id: str | None = Field(
        default=None,
        sa_column_kwargs={"type_": None},
        foreign_key="folders.id",
    )
    created_by: str = Field(foreign_key="users.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )

    child_folders: list["Folder"] = Relationship(
        back_populates="parent_folder",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin",
            "foreign_keys": "[Folder.parent_id]",
        },
    )
    parent_folder: Optional["Folder"] = Relationship(
        back_populates="child_folders",
        sa_relationship_kwargs={"remote_side": "Folder.id", "foreign_keys": "[Folder.parent_id]"},
    )
    files: list["ManagedFile"] = Relationship(
        back_populates="folder",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"},
    )
    created_by_user: Optional["User"] = Relationship(back_populates="folders")


class ManagedFile(SQLModel, table=True):
    __tablename__ = "managed_files"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    original_name: str
    mime_type: str
    size: int
    storage_path: str
    folder_id: str | None = Field(default=None, foreign_key="folders.id")
    status: str = Field(default="ready")
    uploaded_by: str = Field(foreign_key="users.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )

    folder: Optional[Folder] = Relationship(back_populates="files")
    uploaded_by_user: Optional["User"] = Relationship(back_populates="files")


class FileTag(SQLModel, table=True):
    __tablename__ = "file_tags"
    __table_args__ = (UniqueConstraint("file_id", "tag", name="uq_file_tag"),)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    file_id: str = Field(
        sa_column=Column(
            String, ForeignKey("managed_files.id", ondelete="CASCADE"), nullable=False
        ),
    )
    tag: str


class FileMetadata(SQLModel, table=True):
    __tablename__ = "file_metadata"
    __table_args__ = (UniqueConstraint("file_id", "key", name="uq_file_metadata_key"),)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    file_id: str = Field(
        sa_column=Column(
            String, ForeignKey("managed_files.id", ondelete="CASCADE"), nullable=False
        ),
    )
    key: str
    value: str
