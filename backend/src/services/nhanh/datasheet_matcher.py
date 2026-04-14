"""Two-layer product matching: Nhanh products → datasheet files.

Layer 1: Exact code match (NhanhProduct.code vs datasheet folder name).
Layer 2: LLM-based name match using product name vs datasheet content summaries.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger
from pydantic import BaseModel

from src.db.models.nhanh import NhanhProduct
from src.services.llms.models import llm_invoke
from src.services.prompts.service import get_prompt_service

_MODEL_NAME = "services/datasheet_matcher/default"
_PROMPT_NAME = "services.datasheet_matcher"
_LLM_BATCH_SIZE = 20


def _normalize(name: str) -> str:
    return re.sub(r"[\s\-_]+", "", name).lower().strip()


# --- Data classes ---


@dataclass
class DatasheetEntry:
    folder_name: str
    relative_path: str
    normalized: str = ""

    def __post_init__(self):
        if not self.normalized:
            self.normalized = _normalize(self.folder_name)


@dataclass
class MatchResult:
    nhanh_id: int
    product_name: str
    datasheet_path: str | None
    match_layer: str  # "code_exact" | "llm" | "unmatched"
    confidence: str = "high"


class LLMMatchItem(BaseModel):
    nhanh_id: int
    datasheet_path: str  # relative path or "no_match"
    confidence: str


class LLMMatchOutput(BaseModel):
    matches: list[LLMMatchItem]


# --- Index functions ---


def scan_datasheets(datasheets_dir: str) -> list[DatasheetEntry]:
    root = Path(datasheets_dir)
    if not root.exists():
        logger.warning(f"Datasheets directory not found: {datasheets_dir}")
        return []

    entries = []
    for md_file in root.rglob("*.md"):
        relative = md_file.relative_to(root)
        if len(relative.parts) < 2:
            continue
        entries.append(DatasheetEntry(
            folder_name=relative.parts[-2],
            relative_path=str(relative),
        ))

    logger.info(f"Scanned {len(entries)} datasheets from {datasheets_dir}")
    return entries


def _read_summary(datasheets_dir: str, relative_path: str, max_lines: int = 40) -> str:
    try:
        text = (Path(datasheets_dir) / relative_path).read_text(encoding="utf-8")
        return "\n".join(text.splitlines()[:max_lines])
    except Exception as e:
        logger.warning(f"Could not read datasheet {relative_path}: {e}")
        return ""


def _build_catalog_text(datasheets_dir: str, index: list[DatasheetEntry]) -> str:
    summaries = []
    for entry in index:
        summary = _read_summary(datasheets_dir, entry.relative_path)
        if summary:
            summaries.append(
                f"**Path:** `{entry.relative_path}`\n"
                f"**Folder:** {entry.folder_name}\n"
                f"**Summary:**\n{summary}\n"
            )
    return "\n---\n".join(summaries)


# --- LLM call ---


def _build_user_prompt(products: list[NhanhProduct], catalog_text: str) -> str:
    product_lines = [
        f'- ID: {p.nhanh_id}, Name: "{p.name}", Code: "{p.code}"'
        for p in products
    ]
    return (
        f"## Nhanh Products to Match\n\n"
        f"{chr(10).join(product_lines)}\n\n"
        f"## Available Datasheets\n\n{catalog_text}"
    )


async def _call_llm(user_prompt: str) -> LLMMatchOutput | None:
    system_prompt = get_prompt_service().get_prompt(_PROMPT_NAME, use_local_only=True)
    if not system_prompt:
        logger.error(f"Failed to load prompt: {_PROMPT_NAME}")
        return None

    try:
        return await llm_invoke(
            model_name=_MODEL_NAME,
            schema=LLMMatchOutput,
            user_prompt=user_prompt,
            system_prompt=system_prompt,
        )
    except Exception as e:
        logger.error(f"LLM matching failed: {e}")
        return None


def _parse_llm_output(
    products: list[NhanhProduct], output: LLMMatchOutput | None
) -> list[MatchResult]:
    if not output:
        return [_unmatched(p) for p in products]

    llm_map = {m.nhanh_id: m for m in output.matches}
    results = []
    for p in products:
        match = llm_map.get(p.nhanh_id)
        if match and match.datasheet_path != "no_match":
            results.append(MatchResult(
                nhanh_id=p.nhanh_id,
                product_name=p.name,
                datasheet_path=match.datasheet_path,
                match_layer="llm",
                confidence=match.confidence,
            ))
        else:
            results.append(_unmatched(p))
    return results


def _unmatched(p: NhanhProduct) -> MatchResult:
    return MatchResult(
        nhanh_id=p.nhanh_id,
        product_name=p.name,
        datasheet_path=None,
        match_layer="unmatched",
    )


# --- Matcher ---


@dataclass
class DatasheetMatcher:
    datasheets_dir: str
    _index: list[DatasheetEntry] = field(default_factory=list)
    _norm_lookup: dict[str, DatasheetEntry] = field(default_factory=dict)

    def _ensure_index(self):
        if not self._index:
            self._index = scan_datasheets(self.datasheets_dir)
            self._norm_lookup = {e.normalized: e for e in self._index}

    async def match_products(
        self, products: list[NhanhProduct], code_match_only: bool = False
    ) -> list[MatchResult]:
        self._ensure_index()

        results, unmatched = self._code_match_all(products)

        logger.info(f"Layer 1 (code match): {len(results)} matched, {len(unmatched)} unmatched")

        if unmatched and not code_match_only:
            llm_results = await self._llm_match_all(unmatched)
            results.extend(llm_results)
        elif unmatched:
            results.extend([_unmatched(p) for p in unmatched])

        return results

    def _code_match_all(
        self, products: list[NhanhProduct]
    ) -> tuple[list[MatchResult], list[NhanhProduct]]:
        matched = []
        unmatched = []
        for product in products:
            entry = self._code_match_one(product)
            if entry:
                matched.append(MatchResult(
                    nhanh_id=product.nhanh_id,
                    product_name=product.name,
                    datasheet_path=entry.relative_path,
                    match_layer="code_exact",
                ))
            else:
                unmatched.append(product)
        return matched, unmatched

    def _code_match_one(self, product: NhanhProduct) -> DatasheetEntry | None:
        if not product.code:
            return None

        normalized = _normalize(product.code)
        if not normalized:
            return None

        entry = self._norm_lookup.get(normalized)
        if entry:
            return entry

        code_lower = product.code.strip().lower()
        for e in self._index:
            if e.folder_name.strip().lower() == code_lower:
                return e

        return None

    async def _llm_match_all(self, products: list[NhanhProduct]) -> list[MatchResult]:
        catalog_text = _build_catalog_text(self.datasheets_dir, self._index)

        results = []
        for i in range(0, len(products), _LLM_BATCH_SIZE):
            batch = products[i : i + _LLM_BATCH_SIZE]
            prompt = _build_user_prompt(batch, catalog_text)
            output = await _call_llm(prompt)
            results.extend(_parse_llm_output(batch, output))

        matched = sum(1 for r in results if r.match_layer == "llm")
        logger.info(f"Layer 2 (LLM match): {matched} matched, {len(results) - matched} unmatched")

        return results
