"""Utilities for parsing and comparing transmission distances.

Used by generate_bom to guard against a specific class of agent error:
the LLM correctly captures the requested distance in the item notes
(e.g. "120km DDM") but selects a SKU for a different distance variant
(e.g. SFP-1G-40KM-D). This module extracts distances from free text and
detects clear conflicts between the requested distance and the resolved
SKU's max_distance.

Design principle: be conservative. Only report a conflict when BOTH sides
express clear, unambiguous distances that do NOT overlap. Anything fuzzy
(custom lengths like "L meters", multi-value fields, unparseable text)
is treated as "no conflict" so we never block a legitimate BOM.
"""

from __future__ import annotations

import re

# Matches a number (int or decimal) immediately followed by a km/m unit.
# Examples: "120km", "40 km", "0.5km", "300m", "100 m", "3M", "1m".
_DISTANCE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(km|m)\b", re.IGNORECASE)


def extract_distances_meters(text: str | None) -> set[float]:
    """Extract all distances mentioned in ``text``, normalized to meters.

    Returns an empty set if no clear distance token is found.
    """
    if not text:
        return set()

    meters: set[float] = set()
    for value, unit in _DISTANCE_RE.findall(text):
        try:
            num = float(value)
        except ValueError:
            continue
        if unit.lower() == "km":
            num *= 1000.0
        meters.add(num)
    return meters


def is_multivalue_or_fuzzy(max_distance: str | None) -> bool:
    """Return True if the SKU distance field is ambiguous or multi-valued.

    Fields like "300m (OM3), 400m (OM4)", "L meters", "N/A", or an empty
    string cannot be reliably compared to a single requested distance, so
    the caller should skip the conflict check for them.
    """
    if not max_distance:
        return True
    text = max_distance.strip()
    if not text or text.upper() == "N/A":
        return True
    # More than one distinct distance value means it's a range/variant list.
    if len(extract_distances_meters(text)) > 1:
        return True
    # Custom/parametric lengths (patchcords etc.): "L meters", "X meters".
    if re.search(r"\b[lx]\s*met", text, re.IGNORECASE):
        return True
    return False


def find_distance_conflict(
    requested_text: str | None,
    sku_max_distance: str | None,
) -> tuple[float, float] | None:
    """Detect a clear distance conflict between a request and a resolved SKU.

    Args:
        requested_text: Free text describing what the customer asked for
            (typically the item's notes and/or device_model).
        sku_max_distance: The ``max_distance`` value of the resolved Product.

    Returns:
        A ``(requested_meters, sku_meters)`` tuple describing the closest
        conflicting pair when the request and the SKU clearly disagree on
        distance, otherwise ``None``.

    A conflict is reported only when:
      * the request names exactly one clear distance,
      * the SKU has a single, non-fuzzy distance, and
      * the two values are not equal (allowing a small tolerance).
    """
    if is_multivalue_or_fuzzy(sku_max_distance):
        return None

    requested = extract_distances_meters(requested_text)
    sku = extract_distances_meters(sku_max_distance)

    if not requested or not sku:
        return None

    # Only act on an unambiguous single requested distance to avoid
    # misreading descriptions that happen to contain several numbers.
    if len(requested) != 1:
        return None

    req_val = next(iter(requested))
    sku_val = next(iter(sku))

    # Allow a small relative tolerance (5%) for rounding differences.
    tolerance = max(1.0, sku_val * 0.05)
    if abs(req_val - sku_val) <= tolerance:
        return None

    return (req_val, sku_val)


def format_meters(value: float) -> str:
    """Format a distance in meters back into a human-readable km/m string."""
    if value >= 1000 and value % 1000 == 0:
        return f"{int(value // 1000)}km"
    if value >= 1000:
        return f"{value / 1000:g}km"
    return f"{value:g}m"
