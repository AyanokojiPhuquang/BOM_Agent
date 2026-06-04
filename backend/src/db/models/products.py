"""Local product catalog model.

Stores product specifications extracted from uploaded datasheets.
Each row represents one product (a single PDF may contain multiple products).
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Text
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    code: str = Field(index=True, description="Product code / SKU, e.g. SFP-10G-LR, MES3500I-10P")
    name: str = Field(default="", description="Full product name")
    brand: str = Field(default="", description="Manufacturer/brand, e.g. ModuleTek, Eltex, Starview")
    description: str = Field(default="", sa_column=Column(Text), description="Product description in Vietnamese")
    data_rate: str = Field(default="", description="Data rate, e.g. 1G, 10G, 25G, 100G")
    fiber_type: str = Field(default="", description="Fiber type: single-mode, multi-mode, copper, N/A")
    wavelength: str = Field(default="", description="Wavelength, e.g. 1310nm, 850nm, N/A")
    max_distance: str = Field(default="", description="Max transmission distance, e.g. 10km, 300m, N/A")
    connector: str = Field(default="", description="Connector type, e.g. LC Duplex, MPO/MTP, RJ-45, N/A")
    main_device: str = Field(default="", description="Compatible main device/vendor, e.g. Cisco, Juniper, Arista, Eltex, or N/A")
    category: str = Field(default="", description="Product category, e.g. SFP, QSFP, Switch, Media Converter")
    datasheet_path: str | None = Field(default=None, description="Datasheet file path relative to datasheets root")
    pdf_url: str | None = Field(default=None, description="Download URL for the original PDF datasheet")
    raw_specs: str = Field(default="", sa_column=Column(Text), description="Additional specs as free text (for LLM context)")
    status: int = Field(default=1)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
