"""Pydantic schemas for BOM/quotation generation tool.

Defines the input/output contracts for the generate_bom tool
and its internal LLM subagent.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


# --- Tool Input Schemas ---


class BomProductItem(BaseModel):
    """A single product item for quotation generation."""

    product_code: str = Field(
        description="Product code, e.g. MS885DT2XW, TLG04301V.",
    )
    quantity: int = Field(default=1, description="Number of units needed")
    notes: str | None = Field(default=None, description="Additional notes")


class GenerateBomInput(BaseModel):
    """Input schema for the generate_bom tool."""

    customer_name: str = Field(description="Customer or company name")
    customer_phone: str = Field(description="Customer phone number")
    customer_email: str = Field(default="", description="Customer email")
    customer_address: str = Field(default="", description="Customer address")
    items: list[BomProductItem] = Field(description="List of products to include")


# --- Subagent Output Schemas ---


class BomValidationIssue(BaseModel):
    """A missing or ambiguous requirement flagged by the subagent."""

    field: str = Field(description="The requirement field with an issue")
    message: str = Field(description="Description of the issue")
    severity: Literal["warning", "error"] = Field(
        description="error = cannot proceed; warning = assumed a default"
    )


class BomLineItem(BaseModel):
    """One line in the generated quotation."""

    line: int = Field(description="Line item number, starting from 1")
    product_code: str = Field(description="Product code")
    product_name: str = Field(description="Product name")
    image_url: str = Field(default="", description="Product image URL")
    category: str = Field(default="", description="Product category")
    description: str = Field(default="", description="Function/size description")
    quantity: int = Field(description="Number of units")
    unit: str = Field(default="cái", description="Unit of measure")
    unit_price: float = Field(default=0, description="Unit price (VND, VAT included)")
    discount_percent: float = Field(default=0, description="Discount percentage")
    notes: str | None = Field(default=None, description="Notes")


class GenerateBomOutput(BaseModel):
    """Full structured quotation output from the subagent."""

    is_valid: bool = Field(description="False if critical information is missing")
    validation_issues: list[BomValidationIssue] = Field(default_factory=list)
    customer_name: str = Field(description="Customer or company name")
    customer_phone: str = Field(default="", description="Customer phone number")
    customer_email: str = Field(default="", description="Customer email")
    customer_address: str = Field(default="", description="Customer address")
    line_items: list[BomLineItem] = Field(default_factory=list)
    assumptions: list[str] = Field(
        default_factory=list, description="Assumptions made when info was missing"
    )
    summary: str = Field(description="Human-readable summary")


# --- Inventory Tool Input Schema ---


class CheckInventoryInput(BaseModel):
    """Input schema for the check_inventory tool."""

    product_code: str = Field(
        description="Product code, e.g. MS885DT2XW, TLG04301V.",
    )
    quantity: int = Field(default=1, description="Number of units to check availability for")


# --- Inventory Status Schema ---


class ProductInventoryStatus(BaseModel):
    """Real-time inventory status for a product."""

    product_code: str = Field(description="Product code")
    nhanh_product_name: str | None = Field(default=None, description="Product name")
    nhanh_id: int | None = Field(default=None, description="Nhanh product ID")
    quantity_requested: int = Field(description="Quantity requested")
    available: int = Field(default=0, description="Available stock")
    remain: int = Field(default=0, description="Total remaining stock")
    is_sufficient: bool = Field(default=False, description="True if available >= quantity_requested")
    status_label: str = Field(
        default="no_data",
        description="in_stock | partial | out_of_stock | no_data | error",
    )
    error_message: str | None = Field(default=None, description="Error details")


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

    reason: str = Field(description="Brief explanation of why escalating")
    category: EscalationCategory = Field(description="Escalation category")
    conversation_summary: str = Field(description="Summary of the conversation")


# --- Shared constants ---

STATUS_LABELS: dict[str, str] = {
    "in_stock": "Còn hàng",
    "partial": "Không đủ",
    "out_of_stock": "Hết hàng",
    "no_data": "Chưa có dữ liệu",
    "error": "Lỗi",
}
