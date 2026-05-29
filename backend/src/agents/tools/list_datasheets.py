"""Tool to list uploaded datasheets/PDFs with download links."""

from pathlib import Path

from langchain_core.tools import tool

from src.configs import SETTINGS


@tool
async def list_uploaded_datasheets() -> str:
    """List all uploaded PDF datasheets with download links.

    Call this tool when the customer asks to see, download, or get
    all uploaded datasheets/documents/PDFs.

    Returns:
        A formatted list of all uploaded PDFs with download links.
    """
    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()
    files = []

    if datasheets_dir.exists():
        for pdf_file in sorted(datasheets_dir.rglob("*.pdf")):
            relative = pdf_file.relative_to(datasheets_dir)
            parts = relative.parts
            category = parts[0] if len(parts) > 1 else "general"
            size_kb = pdf_file.stat().st_size / 1024
            files.append({
                "filename": pdf_file.name,
                "category": category,
                "size_kb": round(size_kb, 1),
                "download_url": f"/api/datasheets/pdfs/{relative}",
            })

    if not files:
        return "Hiện tại chưa có tài liệu PDF nào được upload lên hệ thống."

    lines = [f"**Tài liệu đã upload ({len(files)} file):**\n"]
    for f in files:
        lines.append(f"- [{f['filename']}]({f['download_url']}) ({f['category']}, {f['size_kb']} KB)")

    return "\n".join(lines)
