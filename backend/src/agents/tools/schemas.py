"""Pydantic schemas for BOM generation tool.

Defines the input/output contracts for the generate_bom tool
and its internal LLM subagent.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


# --- Tool Input Schemas ---


class BomProductItem(BaseModel):
    """A single product item for BOM generation."""

    product_code: str = Field(
        description="Product code/part number, e.g. SFP-10G-ER, SFP-10G-ZR-I.",
    )
    quantity: int = Field(default=1, description="Number of units needed")
    vendor: str = Field(description="Target vendor for coding, e.g. Cisco, Juniper, Fortinet, HPE, Dell")
    device_model: str | None = Field(default=None, description="Device model, e.g. Catalyst 9300")
    notes: str | None = Field(default=None, description="Additional notes or constraints")


class GenerateBomInput(BaseModel):
    """Input schema for the generate_bom tool."""

    customer_name: str = Field(description="Customer or company name")
    customer_phone: str = Field(description="Customer phone number")
    items: list[BomProductItem] = Field(description="List of products to include in the BOM")


# --- Subagent Output Schemas ---


class BomValidationIssue(BaseModel):
    """A missing or ambiguous requirement flagged by the subagent."""

    field: str = Field(description="The requirement field with an issue")
    message: str = Field(description="Description of the issue")
    severity: Literal["warning", "error"] = Field(description="error = cannot proceed; warning = assumed a default")


class BomLineItem(BaseModel):
    """One line in the generated BOM."""

    line: int = Field(description="Line item number, starting from 1")
    sku: str = Field(description="Starview or ModuleTek part number")
    brand: str = Field(description="Product brand: Starview or ModuleTek")
    description: str = Field(description="Product description")
    vendor_compatibility: str = Field(description="Target vendor this transceiver is coded for")
    data_rate: str = Field(description="Data rate, e.g. 10G")
    fiber_type: str = Field(description="single-mode or multi-mode")
    wavelength: str | None = Field(default=None, description="Wavelength, e.g. 850nm, 1310nm")
    max_distance: str = Field(description="Maximum transmission distance")
    connector: str = Field(description="Connector type")
    quantity: int = Field(description="Number of units")
    unit_price_usd: float | None = Field(default=None, description="Unit price in USD, if available")
    notes: str | None = Field(default=None, description="Compatibility notes or caveats")


class GenerateBomOutput(BaseModel):
    """Full structured BOM output from the subagent."""

    is_valid: bool = Field(description="False if critical information is missing to generate a BOM")
    validation_issues: list[BomValidationIssue] = Field(default_factory=list)
    customer_name: str = Field(description="Customer or company name")
    customer_phone: str = Field(default="", description="Customer phone number")
    line_items: list[BomLineItem] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list, description="Assumptions made when info was missing")
    summary: str = Field(description="Human-readable summary of the BOM")


# --- Inventory Tool Input Schema ---


class CheckInventoryInput(BaseModel):
    """Input schema for the check_inventory tool."""

    product_code: str = Field(
        description="Product code, e.g. SFP-10G-ER, SFP-10G-ZR-I. "
        "This is the product model/part number.",
    )
    quantity: int = Field(default=1, description="Number of units to check availability for")


# --- Inventory Status Schema ---


class ProductInventoryStatus(BaseModel):
    """Real-time inventory status for a BOM line item."""

    product_code: str = Field(description="Product code")
    nhanh_product_name: str | None = Field(default=None, description="Product name in Nhanh")
    nhanh_id: int | None = Field(default=None, description="Nhanh product ID")
    quantity_requested: int = Field(description="Quantity requested in BOM")
    available: int = Field(default=0, description="Available stock from Nhanh API")
    remain: int = Field(default=0, description="Total remaining stock from Nhanh API")
    is_sufficient: bool = Field(default=False, description="True if available >= quantity_requested")
    status_label: str = Field(
        default="no_data",
        description="in_stock | partial | out_of_stock | no_data | error",
    )
    error_message: str | None = Field(default=None, description="Error details when status is 'error'")


# --- Escalation Schemas ---


class EscalationCategory(str, Enum):
    """Categories for escalation to human support."""

    OFF_TOPIC = "off_topic"
    TOO_COMPLEX = "too_complex"
    CUSTOMER_COMPLAINT = "customer_complaint"
    PRICING_REQUEST = "pricing_request"
    URGENT_TECHNICAL = "urgent_technical"
    OTHER = "other"


class EscalateInput(BaseModel):
    """Input schema for the escalate_to_human tool."""

    reason: str = Field(description="Brief explanation of why this conversation is being escalated")
    category: EscalationCategory = Field(description="Escalation category")
    conversation_summary: str = Field(description="Summary of the conversation so far, including what the customer needs")


# --- Shared constants ---

STATUS_LABELS: dict[str, str] = {
    "in_stock": "In Stock",
    "partial": "Partial",
    "out_of_stock": "Out of Stock",
    "no_data": "No Data",
    "error": "Error",
}


