import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class NhanhToken(SQLModel, table=True):
    __tablename__ = "nhanh_tokens"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    business_id: str = Field(index=True)
    access_token: str
    expired_at: int  # Unix timestamp
    depot_ids: str | None = None  # JSON array string
    page_ids: str | None = None  # JSON array string
    permissions: str | None = None  # JSON array string
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )


class NhanhSyncLog(SQLModel, table=True):
    __tablename__ = "nhanh_sync_logs"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    sync_type: str = "full"  # "full" or "incremental"
    total_created: int = 0
    total_updated: int = 0
    total_pages_fetched: int = 0
    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    finished_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )


class NhanhProduct(SQLModel, table=True):
    __tablename__ = "nhanh_products"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    nhanh_id: int = Field(unique=True, index=True)
    parent_id: int | None = None
    name: str = ""
    code: str = ""
    barcode: str = ""
    price: float = 0
    import_price: float = 0
    category_id: int | None = None
    brand_id: int | None = None
    status: int = 0
    remain: int = 0
    available: int = 0
    image: str = ""
    datasheet_path: str | None = Field(default=None, description="Matched datasheet file path relative to datasheets root")
    last_synced_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
