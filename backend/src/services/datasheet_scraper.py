"""AI-driven datasheet link discovery and download.

Given a product page URL, this service:
    1. Fetches the page HTML.
    2. Extracts every candidate link / button (anchors, buttons with onclick,
       elements whose text or attributes hint at a datasheet download).
    3. Asks an LLM to pick the single link that points to the product's
       datasheet — this is layout-agnostic, so it works across sites with
       completely different markup (no brittle CSS/XPath auto-clicking).
    4. Resolves & downloads the chosen file (streaming, size-capped).

The downloaded file is then fed into the SAME processing pipeline used by the
direct PDF upload and Google Drive sync flows (pdf_to_markdown ->
extract_product_specs_from_content -> _sync_products_from_datasheets).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from loguru import logger
from pydantic import BaseModel, Field

# --- Constants ---

MAX_HTML_SIZE = 5 * 1024 * 1024  # 5MB of HTML is plenty
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB download cap (matches drive worker)
DOWNLOAD_CHUNK_SIZE = 64 * 1024  # 64KB
FETCH_TIMEOUT = 30.0
DOWNLOAD_TIMEOUT = 120.0
RENDER_TIMEOUT = 45.0  # headless browser page load timeout (seconds)
MAX_CANDIDATES = 120  # cap the number of links sent to the LLM

_SCRAPER_MODEL = "services/datasheet_scraper/default"

# File extensions we consider to be downloadable datasheets.
_DATASHEET_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx")

# Keywords that hint a link is a datasheet download (used only to enrich
# candidate metadata for the LLM — the LLM makes the final decision).
_HINT_KEYWORDS = (
    "datasheet", "data sheet", "data-sheet", "spec", "specification",
    "download", "brochure", "manual", "document", "pdf", "tài liệu",
    "thông số", "tải", "catalog", "catalogue",
)

_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


# --- Errors ---


class DatasheetScrapeError(Exception):
    """Raised when a datasheet link cannot be found or downloaded."""


# --- Link extraction ---


@dataclass
class LinkCandidate:
    """A candidate download link discovered on the page."""

    url: str
    text: str = ""
    attrs: str = ""

    def to_prompt_line(self, index: int) -> str:
        text = self.text.strip()[:120]
        attrs = self.attrs.strip()[:160]
        return f"[{index}] url={self.url} | text={text!r} | hints={attrs!r}"


class _LinkExtractor(HTMLParser):
    """Collects candidate download links from HTML.

    Uses the stdlib HTML parser (no extra dependency). It records anchors and
    any element carrying URL-bearing attributes (href, data-href, data-file,
    onclick=...). Nearby text is associated with the most recent link.
    """

    _URL_ATTRS = ("href", "data-href", "data-file", "data-url", "data-download", "src")

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.candidates: list[LinkCandidate] = []
        self._current: LinkCandidate | None = None
        self._depth_of_current: int = 0
        self._depth: int = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._depth += 1
        attr_map = {k.lower(): (v or "") for k, v in attrs}

        found_url: str | None = None
        for a in self._URL_ATTRS:
            if attr_map.get(a):
                found_url = attr_map[a]
                break

        # Extract a URL embedded in an onclick handler, e.g.
        # onclick="window.open('/files/spec.pdf')"
        if not found_url and attr_map.get("onclick"):
            m = re.search(r"""["']([^"']+\.(?:pdf|docx?|xlsx?))["']""", attr_map["onclick"], re.I)
            if m:
                found_url = m.group(1)

        if found_url:
            hint_parts = []
            for key in ("title", "aria-label", "class", "id", "download", "type"):
                if attr_map.get(key):
                    hint_parts.append(f"{key}={attr_map[key]}")
            candidate = LinkCandidate(url=found_url, attrs=" ".join(hint_parts))
            self.candidates.append(candidate)
            self._current = candidate
            self._depth_of_current = self._depth

    def handle_endtag(self, tag: str) -> None:
        if self._current is not None and self._depth <= self._depth_of_current:
            self._current = None
        self._depth = max(0, self._depth - 1)

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text and self._current is not None:
            self._current.text = (self._current.text + " " + text).strip()


def extract_link_candidates(html: str, base_url: str) -> list[LinkCandidate]:
    """Parse HTML and return de-duplicated, absolute-URL link candidates.

    Candidates that clearly point to a downloadable document, or whose text /
    attributes hint at a datasheet, are prioritised. All same-page anchors
    (``#...``) and non-http schemes (mailto:, javascript:) are dropped.
    """
    parser = _LinkExtractor()
    try:
        parser.feed(html)
    except Exception as e:  # malformed HTML — keep whatever we parsed
        logger.warning(f"HTML parsing hit an error (continuing with partial results): {e}")

    seen: set[str] = set()
    prioritized: list[LinkCandidate] = []
    others: list[LinkCandidate] = []

    for cand in parser.candidates:
        raw = cand.url.strip()
        if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue

        absolute = urljoin(base_url, raw)
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            continue

        if absolute in seen:
            continue
        seen.add(absolute)

        cand.url = absolute
        blob = f"{absolute} {cand.text} {cand.attrs}".lower()
        is_doc = parsed.path.lower().endswith(_DATASHEET_EXTENSIONS)
        has_hint = any(kw in blob for kw in _HINT_KEYWORDS)

        if is_doc or has_hint:
            prioritized.append(cand)
        else:
            others.append(cand)

    # Prioritised links first, then fill remaining budget with the rest.
    ordered = prioritized + others
    return ordered[:MAX_CANDIDATES]


# --- LLM selection ---


class DatasheetLinkSelection(BaseModel):
    """LLM decision on which candidate link is the product datasheet."""

    found: bool = Field(description="True if a datasheet download link was identified.")
    url: str = Field(default="", description="The absolute URL of the datasheet download link.")
    reason: str = Field(default="", description="Brief reason for the choice, or why none was found.")


_SELECTION_SYSTEM_PROMPT = """You are an assistant that locates the datasheet (technical specification document) download link on a product web page.

You are given a product page URL, its title, and a numbered list of candidate links extracted from the page. Each candidate shows its URL, visible link text, and attribute hints (title, class, id, aria-label, download).

Your job: identify the SINGLE link that downloads the product's datasheet / technical specification document (usually a PDF, sometimes DOC/DOCX/XLS/XLSX).

Rules:
1. Prefer links that point directly to a document file (.pdf, .docx, .xlsx) whose text or attributes mention "datasheet", "data sheet", "specification", "spec", "download", "brochure", "tài liệu", "thông số kỹ thuật".
2. If several documents exist (e.g. datasheet, manual, brochure), pick the one most likely to be the technical DATASHEET / specification for THIS product.
3. Do NOT pick navigation, login, social media, related-product, or image links.
4. If no candidate is a datasheet download, set found=false.
5. Always return the URL exactly as shown in the candidate list (it is already absolute)."""


async def select_datasheet_link(
    url: str,
    page_title: str,
    candidates: list[LinkCandidate],
) -> DatasheetLinkSelection:
    """Ask the LLM to choose the datasheet link among the candidates."""
    from src.services.llms.models import llm_invoke

    if not candidates:
        return DatasheetLinkSelection(found=False, reason="No links found on the page.")

    candidate_block = "\n".join(c.to_prompt_line(i) for i, c in enumerate(candidates))
    user_prompt = (
        f"Product page URL: {url}\n"
        f"Page title: {page_title}\n\n"
        f"Candidate links:\n{candidate_block}\n\n"
        "Return the datasheet download link, or found=false if none applies."
    )

    try:
        selection: DatasheetLinkSelection = await llm_invoke(
            model_name=_SCRAPER_MODEL,
            schema=DatasheetLinkSelection,
            user_prompt=user_prompt,
            system_prompt=_SELECTION_SYSTEM_PROMPT,
        )
    except Exception as e:
        logger.error(f"LLM datasheet link selection failed: {e}")
        raise DatasheetScrapeError(f"Failed to analyze the page with AI: {e}") from e

    # Guard: make sure the LLM returned one of the real candidate URLs.
    if selection.found and selection.url:
        candidate_urls = {c.url for c in candidates}
        if selection.url not in candidate_urls:
            # Try a loose match (LLM may have trimmed a trailing slash etc.)
            match = next(
                (c.url for c in candidates if c.url.rstrip("/") == selection.url.rstrip("/")),
                None,
            )
            if match:
                selection.url = match
            else:
                logger.warning(
                    f"LLM returned a URL not in candidates: {selection.url}. Ignoring."
                )
                return DatasheetLinkSelection(
                    found=False,
                    reason="AI selected a link that was not among the page candidates.",
                )

    return selection


async def find_datasheet_url(url: str) -> DatasheetLinkSelection:
    """Find the datasheet download link for a product URL.

    Strategy (fast path first, then fallback):
      1. Fetch static HTML and let the LLM pick the datasheet link.
      2. If nothing is found (common for JS-rendered / SPA pages), re-fetch
         the page with a headless browser that executes JavaScript, then let
         the LLM try again.

    Returns a DatasheetLinkSelection (``found`` indicates success).
    Raises DatasheetScrapeError on unrecoverable fetch/LLM errors.
    """
    # --- Fast path: static HTML ---
    html, final_url = await fetch_page_html(url)
    candidates = extract_link_candidates(html, final_url)
    page_title = _extract_title(html)
    selection = await select_datasheet_link(final_url, page_title, candidates)

    if selection.found and selection.url:
        return selection

    logger.info(
        f"No datasheet link in static HTML for {url}; retrying with JS rendering."
    )

    # --- Fallback: render with headless browser (executes JS) ---
    try:
        rendered_html, rendered_final = await render_page_html(url)
    except DatasheetScrapeError as e:
        logger.warning(f"JS rendering fallback failed for {url}: {e}")
        # Return the original (not-found) selection with a helpful reason.
        return DatasheetLinkSelection(
            found=False,
            reason=(
                "No datasheet link found in the page HTML, and JavaScript "
                f"rendering could not be used ({e})."
            ),
        )

    rendered_candidates = extract_link_candidates(rendered_html, rendered_final)
    rendered_title = _extract_title(rendered_html) or page_title
    return await select_datasheet_link(rendered_final, rendered_title, rendered_candidates)


def _extract_title(html: str) -> str:
    """Extract the <title> text from HTML (best-effort)."""
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    return m.group(1).strip()[:200] if m else ""


# --- Fetch & download ---


@dataclass
class DownloadedDatasheet:
    """Result of downloading a datasheet file."""

    path: Path
    filename: str
    source_url: str
    content_type: str = ""
    size: int = 0


async def fetch_page_html(url: str) -> tuple[str, str]:
    """Fetch a page and return (html, final_url_after_redirects).

    Raises DatasheetScrapeError on network/HTTP errors.
    """
    _validate_url(url)
    try:
        async with httpx.AsyncClient(
            follow_redirects=True, timeout=FETCH_TIMEOUT, headers=_BROWSER_HEADERS
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")

            # If the URL itself is already a document, there's nothing to scrape.
            if not content_type.startswith("text/") and "html" not in content_type:
                raise DatasheetScrapeError(
                    f"URL does not point to an HTML page (content-type: {content_type}). "
                    "Provide a product page URL, not a direct file link."
                )

            html = response.text[:MAX_HTML_SIZE]
            return html, str(response.url)
    except httpx.HTTPStatusError as e:
        raise DatasheetScrapeError(
            f"Failed to fetch page (HTTP {e.response.status_code})."
        ) from e
    except httpx.HTTPError as e:
        raise DatasheetScrapeError(f"Failed to fetch page: {e}") from e


async def render_page_html(url: str) -> tuple[str, str]:
    """Fetch a page using a headless browser that executes JavaScript.

    This is the fallback for JS-rendered / SPA product pages where the
    datasheet link is injected by client-side scripts and therefore absent
    from the static HTML returned by ``fetch_page_html``.

    Returns (html, final_url_after_redirects).

    Raises DatasheetScrapeError if Playwright is unavailable or rendering fails.
    """
    _validate_url(url)

    try:
        from playwright.async_api import async_playwright
    except ImportError as e:
        raise DatasheetScrapeError(
            "JavaScript rendering is unavailable (Playwright not installed)."
        ) from e

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            try:
                context = await browser.new_context(
                    user_agent=_BROWSER_HEADERS["User-Agent"]
                )
                page = await context.new_page()
                # Wait for the network to settle so JS-injected links are present.
                await page.goto(
                    url, wait_until="networkidle", timeout=int(RENDER_TIMEOUT * 1000)
                )
                # Give late-loading widgets a brief moment.
                await page.wait_for_timeout(1500)
                html = await page.content()
                final_url = page.url
            finally:
                await browser.close()
    except DatasheetScrapeError:
        raise
    except Exception as e:
        raise DatasheetScrapeError(f"Failed to render page with browser: {e}") from e

    return html[:MAX_HTML_SIZE], final_url


async def download_datasheet(url: str, dest_dir: Path) -> DownloadedDatasheet:
    """Stream-download a datasheet file to dest_dir.

    Raises DatasheetScrapeError on failure or if the file exceeds the size cap.
    """
    _validate_url(url)
    dest_dir.mkdir(parents=True, exist_ok=True)

    try:
        async with httpx.AsyncClient(
            follow_redirects=True, timeout=DOWNLOAD_TIMEOUT, headers=_BROWSER_HEADERS
        ) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                filename = _resolve_filename(url, response.headers)
                dest_path = dest_dir / filename

                total = 0
                with open(dest_path, "wb") as f:
                    async for chunk in response.aiter_bytes(DOWNLOAD_CHUNK_SIZE):
                        total += len(chunk)
                        if total > MAX_FILE_SIZE:
                            f.close()
                            dest_path.unlink(missing_ok=True)
                            raise DatasheetScrapeError(
                                f"File exceeds {MAX_FILE_SIZE // (1024 * 1024)}MB limit."
                            )
                        f.write(chunk)

        logger.info(f"Downloaded datasheet {url} ({total} bytes) -> {dest_path}")
        return DownloadedDatasheet(
            path=dest_path,
            filename=filename,
            source_url=url,
            content_type=content_type,
            size=total,
        )
    except httpx.HTTPStatusError as e:
        raise DatasheetScrapeError(
            f"Failed to download datasheet (HTTP {e.response.status_code})."
        ) from e
    except httpx.HTTPError as e:
        raise DatasheetScrapeError(f"Failed to download datasheet: {e}") from e


# --- Helpers ---


def _validate_url(url: str) -> None:
    """Reject non-http(s) URLs to avoid SSRF via file://, etc."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise DatasheetScrapeError(f"Invalid or unsupported URL: {url}")


def _resolve_filename(url: str, headers: httpx.Headers) -> str:
    """Determine a safe filename from Content-Disposition or the URL path."""
    disposition = headers.get("content-disposition", "")
    if disposition:
        m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', disposition, re.I)
        if m:
            name = _sanitize_filename(m.group(1))
            if name:
                return name

    path_name = Path(urlparse(url).path).name
    name = _sanitize_filename(path_name)
    if name:
        # Ensure it has a document extension for the downstream pipeline.
        if not name.lower().endswith(_DATASHEET_EXTENSIONS):
            content_type = headers.get("content-type", "")
            if "pdf" in content_type:
                name += ".pdf"
        return name

    # Fallback name
    content_type = headers.get("content-type", "")
    ext = ".pdf" if "pdf" in content_type else ".bin"
    return f"datasheet{ext}"


def _sanitize_filename(name: str) -> str:
    """Strip path separators and unsafe characters from a filename."""
    name = name.strip().replace("\\", "/").split("/")[-1]
    name = re.sub(r"[^A-Za-z0-9._\- ]+", "_", name).strip()
    return name[:200]
