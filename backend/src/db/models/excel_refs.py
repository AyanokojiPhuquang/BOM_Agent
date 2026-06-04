"""Excel reference file model.

Stores uploaded Excel files and their extracted product code → description mappings.
Used to sync/override product descriptions in the Products table.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlmodel import Field, SQLModel


class ExcelFile(SQLModel, table=True):
    """Represents an uploaded Excel reference file."""
    __tablename__ = "excel_files"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    filename: str = Field(description="Original filename")
    file_size: int = Field(default=0, description="File size in bytes")
    total_rows: int = Field(default=0, description="Number of product rows extracted")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )


class ExcelProductRef(SQLModel, table=True):
    """A single product code → description mapping from an Excel file."""
    __tablename__ = "excel_product_refs"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    excel_file_id: str = Field(foreign_key="excel_files.id", index=True)
    product_code: str = Field(index=True, description="P/N from Excel")
    description: str = Field(default="", sa_column=Column(Text), description="Description from Excel")
