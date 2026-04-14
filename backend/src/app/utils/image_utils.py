"""Utility functions for saving uploaded images to disk."""

import base64
import uuid
from pathlib import Path

from loguru import logger

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_images(images: list[dict]) -> list[str]:
    """Save base64 data URL images to disk.

    Args:
        images: List of image dicts with 'dataUrl' and 'name' keys.

    Returns:
        List of saved file paths (relative to data/).
    """
    saved_paths: list[str] = []

    for img in images:
        data_url: str = img.get("dataUrl", "")
        name: str = img.get("name", "image.png")

        if not data_url or "," not in data_url:
            continue

        # Extract base64 data after the comma
        _, b64_data = data_url.split(",", 1)

        # Determine extension from original filename
        ext = Path(name).suffix or ".png"
        filename = f"{uuid.uuid4()}{ext}"
        file_path = UPLOAD_DIR / filename

        try:
            file_path.write_bytes(base64.b64decode(b64_data))
            saved_paths.append(f"uploads/{filename}")
            logger.debug(f"Saved image: {file_path}")
        except Exception:
            logger.opt(exception=True).warning(f"Failed to save image: {name}")

    return saved_paths
