"""Tool result offloading middleware.

Offloads large tool results to files when context grows beyond a configurable
token threshold, replacing them with a file path reference.

Ported from biota/src/agents/middleware/tool_result_offloading.py.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable, Iterable, Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import gettempdir
from typing import Literal

from langchain.agents.middleware.context_editing import ContextEdit, TokenCounter
from langchain.agents.middleware.types import (
    AgentMiddleware,
    ModelCallResult,
    ModelRequest,
    ModelResponse,
)
from langchain_core.messages import AIMessage, AnyMessage, ToolMessage
from langchain_core.messages.utils import count_tokens_approximately
from loguru import logger

DEFAULT_STORAGE_DIR = Path(gettempdir()) / "tool_result_offloads"

DEFAULT_PLACEHOLDER = (
    "[Content offloaded to reduce context size. "
    "Read from file if needed: {file_path}. "
    "Tool: {tool_name}, Original size: {original_size} chars]"
)


# =============================================================================
# Helper Functions
# =============================================================================


def get_content_as_string(content: str | list) -> str | None:
    """Extract string content from ToolMessage content field."""
    if isinstance(content, str):
        return content

    if not isinstance(content, list):
        return None

    text_parts = []
    for block in content:
        if isinstance(block, str):
            text_parts.append(block)
        elif isinstance(block, dict) and block.get("type") == "text":
            text_parts.append(block.get("text", ""))

    return "\n".join(text_parts) if text_parts else None


def sanitize_filename(name: str) -> str:
    """Convert a string to a safe filename."""
    return "".join(c if c.isalnum() else "_" for c in name)


def generate_file_path(storage_dir: Path, tool_name: str, tool_call_id: str) -> Path:
    """Generate a unique file path for offloaded content."""
    timestamp = int(time.time() * 1000)
    safe_tool_name = sanitize_filename(tool_name)
    safe_call_id = tool_call_id.replace("-", "")[:12] if tool_call_id else "unknown"
    filename = f"{safe_tool_name}_{safe_call_id}_{timestamp}.txt"
    return storage_dir / filename


def write_content_to_file(file_path: Path, content: str) -> bool:
    """Write content to file. Returns True on success."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return True
    except OSError as e:
        logger.warning(f"Failed to write offloaded content to {file_path}: {e}")
        return False


def create_placeholder(
    template: str,
    file_path: Path,
    tool_name: str,
    original_size: int,
) -> str:
    """Create placeholder message with file path reference."""
    return template.format(
        file_path=str(file_path),
        tool_name=tool_name,
        original_size=original_size,
    )


def is_already_offloaded(tool_message: ToolMessage) -> bool:
    """Check if a tool message has already been offloaded."""
    metadata = tool_message.response_metadata.get("context_editing", {})
    return metadata.get("offloaded", False)


def find_tool_call_for_message(
    messages: list[AnyMessage],
    tool_message: ToolMessage,
    message_index: int,
) -> dict | None:
    """Find the AIMessage tool call that corresponds to a ToolMessage."""
    for msg in reversed(messages[:message_index]):
        if not isinstance(msg, AIMessage):
            continue
        for call in msg.tool_calls:
            if call.get("id") == tool_message.tool_call_id:
                return call
    return None


def get_tool_name(tool_message: ToolMessage, tool_call: dict) -> str:
    """Get the tool name from message or tool call."""
    return tool_message.name or tool_call.get("name", "unknown")


def create_offloaded_message(
    tool_message: ToolMessage,
    placeholder: str,
    file_path: Path,
    original_size: int,
) -> ToolMessage:
    """Create a new ToolMessage with offloaded content."""
    return tool_message.model_copy(
        update={
            "content": placeholder,
            "response_metadata": {
                **tool_message.response_metadata,
                "context_editing": {
                    "offloaded": True,
                    "strategy": "offload_tool_results",
                    "file_path": str(file_path),
                    "original_size": original_size,
                },
            },
        }
    )


def get_offload_candidates(
    messages: list[AnyMessage],
    keep: int,
) -> list[tuple[int, ToolMessage]]:
    """Get list of (index, ToolMessage) candidates for offloading."""
    candidates = [(idx, msg) for idx, msg in enumerate(messages) if isinstance(msg, ToolMessage)]

    if keep >= len(candidates):
        return []

    if keep > 0:
        return candidates[:-keep]

    return candidates


# =============================================================================
# Edit Strategy
# =============================================================================


@dataclass(slots=True)
class OffloadToolResultsEdit(ContextEdit):
    """Configuration for offloading tool results to files."""

    trigger: int = 80_000
    """Token count that triggers the offload."""

    min_content_size: int = 500
    """Minimum content size (chars) to consider for offloading."""

    keep: int = 3
    """Number of most recent tool results to preserve."""

    exclude_tools: Sequence[str] = ()
    """Tool names to never offload."""

    storage_dir: Path = field(default_factory=lambda: DEFAULT_STORAGE_DIR)
    """Directory for storing offloaded content."""

    placeholder_template: str = DEFAULT_PLACEHOLDER
    """Template for placeholder message."""

    def apply(
        self,
        messages: list[AnyMessage],
        *,
        count_tokens: TokenCounter,
    ) -> None:
        """Apply the offload-tool-results strategy."""
        if not self._should_trigger(messages, count_tokens):
            return

        candidates = get_offload_candidates(messages, self.keep)
        excluded = set(self.exclude_tools)

        for idx, tool_message in candidates:
            self._process_candidate(messages, idx, tool_message, excluded)

    def _should_trigger(
        self,
        messages: list[AnyMessage],
        count_tokens: TokenCounter,
    ) -> bool:
        """Check if offloading should be triggered."""
        return count_tokens(messages) > self.trigger

    def _process_candidate(
        self,
        messages: list[AnyMessage],
        idx: int,
        tool_message: ToolMessage,
        excluded: set[str],
    ) -> None:
        """Process a single candidate for offloading."""
        if is_already_offloaded(tool_message):
            return

        content = get_content_as_string(tool_message.content)
        if content is None:
            return

        if len(content) < self.min_content_size:
            return

        tool_call = find_tool_call_for_message(messages, tool_message, idx)
        if tool_call is None:
            return

        tool_name = get_tool_name(tool_message, tool_call)
        if tool_name in excluded:
            return

        self._offload_message(messages, idx, tool_message, tool_name, content)

    def _offload_message(
        self,
        messages: list[AnyMessage],
        idx: int,
        tool_message: ToolMessage,
        tool_name: str,
        content: str,
    ) -> None:
        """Offload a tool message to file and update messages list."""
        file_path = generate_file_path(
            self.storage_dir,
            tool_name,
            tool_message.tool_call_id,
        )

        if not write_content_to_file(file_path, content):
            return

        placeholder = create_placeholder(
            self.placeholder_template,
            file_path,
            tool_name,
            len(content),
        )

        messages[idx] = create_offloaded_message(
            tool_message,
            placeholder,
            file_path,
            len(content),
        )

        logger.debug(f"Offloaded tool result '{tool_name}' ({len(content)} chars) to {file_path}")


# =============================================================================
# Middleware
# =============================================================================


class ToolResultOffloadingMiddleware(AgentMiddleware):
    """Automatically offload large tool results to files to manage context size.

    When the total token count exceeds the configured threshold, this middleware
    writes large tool results to files and replaces them with a placeholder
    containing the file path.
    """

    edits: list[ContextEdit]
    token_count_method: Literal["approximate", "model"]

    def __init__(
        self,
        *,
        edits: Iterable[ContextEdit] | None = None,
        token_count_method: Literal["approximate", "model"] = "approximate",
    ) -> None:
        super().__init__()
        self.edits = list(edits or (OffloadToolResultsEdit(),))
        self.token_count_method = token_count_method

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelCallResult:
        """Apply offloading before invoking the model."""
        edited_request = self._apply_edits(request)
        return handler(edited_request)

    async def awrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], Awaitable[ModelResponse]],
    ) -> ModelCallResult:
        """Apply offloading before invoking the model (async)."""
        edited_request = self._apply_edits(request)
        return await handler(edited_request)

    def _apply_edits(self, request: ModelRequest) -> ModelRequest:
        """Apply all edits to the request messages."""
        if not request.messages:
            return request

        count_tokens = self._create_token_counter(request)
        edited_messages = deepcopy(list(request.messages))

        for edit in self.edits:
            edit.apply(edited_messages, count_tokens=count_tokens)

        return request.override(messages=edited_messages)

    def _create_token_counter(self, request: ModelRequest) -> TokenCounter:
        """Create a token counting function based on configured method."""
        if self.token_count_method == "approximate":
            return self._approximate_counter

        return self._create_model_counter(request)

    def _approximate_counter(self, messages: Sequence) -> int:
        """Count tokens using approximate method."""
        return count_tokens_approximately(list(messages))

    def _create_model_counter(self, request: ModelRequest) -> TokenCounter:
        """Create a token counter using the model."""
        system_msg = [request.system_message] if request.system_message else []

        def counter(messages: Sequence) -> int:
            return request.model.get_num_tokens_from_messages(
                system_msg + list(messages),
                request.tools,
            )

        return counter
