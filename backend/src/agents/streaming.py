"""Streaming utilities for the BOM assistant agent.

Provides streaming functionality with typed events.
Handles message processing during astream to filter and yield only relevant content.
Supports text chunks, tool calls, tool results, thinking, and usage metrics.

Ported from biota/src/agents/streaming.py.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from langchain_core.messages import AIMessage, AIMessageChunk, ToolMessage


# ============================================================================
# Constants
# ============================================================================

STREAMABLE_NODES: tuple = (
    "agent",
    "model",
)


# ============================================================================
# Stream Event Types
# ============================================================================


@dataclass
class StreamChunk:
    """A chunk of streamed text content."""

    content: str


@dataclass
class StreamToolCall:
    """A tool call initiated by the agent."""

    name: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamToolResult:
    """A tool result returned after execution."""

    name: str
    content: str
    status: str = "ok"


@dataclass
class StreamUsage:
    """Token usage from an LLM call."""

    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0


@dataclass
class StreamThinking:
    """A chunk of reasoning/thinking content from the model."""

    content: str


@dataclass
class StreamTraceUrl:
    """Trace URL for observability."""

    url: str


StreamEvent = StreamChunk | StreamToolCall | StreamToolResult | StreamUsage | StreamThinking | StreamTraceUrl


# ============================================================================
# Helper Functions
# ============================================================================


def is_streamable_node(node_name: str) -> bool:
    """Check if the node should produce streamable content."""
    return node_name in STREAMABLE_NODES


def has_tool_calls(msg: AIMessage) -> bool:
    """Check if the message has tool calls."""
    return hasattr(msg, "tool_calls") and bool(msg.tool_calls)


# ============================================================================
# Stream Message Processing
# ============================================================================


class StreamEventProcessor:
    """Processes stream messages into typed events including tool activity.

    Yields StreamChunk, StreamToolCall, StreamToolResult, StreamThinking,
    and StreamUsage events for rich clients that want full visibility.

    Accumulates streamed tool call chunks (name arrives first, then args)
    and emits a single StreamToolCall once the call is complete.
    """

    def __init__(self):
        self._pending_tool_name: str = ""
        self._pending_tool_args: dict[str, Any] = {}

    def process_message(
        self,
        msg: Any,
        node_name: str,
    ) -> Optional[StreamEvent | List[StreamEvent]]:
        """Process a stream message and return typed event(s) if relevant."""
        if isinstance(msg, ToolMessage):
            return self._process_tool_result(msg)

        if not isinstance(msg, (AIMessage, AIMessageChunk)):
            return None
        if not is_streamable_node(node_name):
            return None

        events: list[StreamEvent] = []
        events.extend(self._extract_usage(msg))
        events.extend(self._extract_thinking(msg))
        events.extend(self._process_tool_calls_or_content(msg))

        if len(events) == 1:
            return events[0]
        return events or None

    # -- Tool result handling --------------------------------------------------

    def _process_tool_result(self, msg: ToolMessage) -> StreamEvent | List[StreamEvent]:
        """Convert a ToolMessage into StreamToolResult, flushing pending calls first."""
        events: list[StreamEvent] = []
        self._flush_pending_tool_call(events)
        events.append(
            StreamToolResult(
                name=msg.name or "unknown",
                content=str(msg.content),
                status=getattr(msg, "status", "ok") or "ok",
            )
        )
        return events if len(events) > 1 else events[0]

    # -- Usage extraction ------------------------------------------------------

    @staticmethod
    def _extract_usage(msg: AIMessage) -> list[StreamUsage]:
        """Extract token usage metadata from an AI message."""
        usage = getattr(msg, "usage_metadata", None)
        if not usage or not (usage.get("input_tokens") or usage.get("output_tokens")):
            return []

        input_detail = usage.get("input_token_details", {}) or {}
        output_detail = usage.get("output_token_details", {}) or {}
        return [
            StreamUsage(
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
                reasoning_tokens=output_detail.get("reasoning", 0),
                cache_read_tokens=input_detail.get("cache_read", 0),
                cache_creation_tokens=input_detail.get("cache_creation", 0),
            )
        ]

    # -- Thinking / reasoning extraction ---------------------------------------

    @staticmethod
    def _extract_thinking(msg: AIMessage) -> list[StreamThinking]:
        """Extract reasoning/thinking content from additional_kwargs."""
        additional_kwargs = getattr(msg, "additional_kwargs", {}) or {}
        events: list[StreamThinking] = []

        # Chat Completions format
        reasoning_content = additional_kwargs.get("reasoning_content")
        if reasoning_content:
            events.append(StreamThinking(content=reasoning_content))

        # Responses API v0 format
        reasoning_block = additional_kwargs.get("reasoning")
        if isinstance(reasoning_block, dict):
            for part in reasoning_block.get("summary", []):
                text = part.get("text", "")
                if text:
                    events.append(StreamThinking(content=text))

        return events

    # -- Tool call accumulation ------------------------------------------------

    def _process_tool_calls_or_content(self, msg: AIMessage) -> list[StreamEvent]:
        """Handle tool call chunks or content blocks from an AI message."""
        events: list[StreamEvent] = []
        tool_calls = getattr(msg, "tool_calls", [])

        # Always process content first so pre-tool text is never dropped
        if msg.content:
            self._flush_pending_tool_call(events)
            events.extend(self._parse_content(msg.content))

        # Then process tool calls
        if tool_calls:
            events.extend(self._accumulate_tool_call(tool_calls[0]))

        return events

    def _accumulate_tool_call(self, tc: dict) -> list[StreamEvent]:
        """Accumulate streamed tool call chunks; emit when complete."""
        events: list[StreamEvent] = []
        name = tc.get("name", "")
        args = tc.get("args", {})

        if name:
            self._flush_pending_tool_call(events)
            self._pending_tool_name = name
            self._pending_tool_args = args or {}
        elif args:
            self._pending_tool_args.update(args)
            self._flush_pending_tool_call(events)
        elif self._pending_tool_name:
            self._flush_pending_tool_call(events)

        return events

    def _flush_pending_tool_call(self, events: list[StreamEvent]) -> None:
        """Emit accumulated tool call if one is pending."""
        if self._pending_tool_name:
            events.append(StreamToolCall(name=self._pending_tool_name, args=self._pending_tool_args))
            self._pending_tool_name = ""
            self._pending_tool_args = {}

    # -- Content parsing -------------------------------------------------------

    @staticmethod
    def _parse_content(content: str | list) -> list[StreamEvent]:
        """Parse message content into StreamChunk and StreamThinking events."""
        if isinstance(content, str):
            return [StreamChunk(content=content)]

        events: list[StreamEvent] = []
        for block in content:
            if isinstance(block, str):
                events.append(StreamChunk(content=block))
            elif isinstance(block, dict):
                events.extend(_parse_content_block(block))
        return events


def _parse_content_block(block: dict) -> list[StreamEvent]:
    """Parse a single typed content block into events."""
    block_type = block.get("type", "")

    if block_type == "reasoning":
        return [StreamThinking(content=part["text"]) for part in block.get("summary", []) if part.get("text")]

    if block_type == "text":
        text = block.get("text", "")
        return [StreamChunk(content=text)] if text else []

    if block_type in ("refusal", "web_search_call"):
        return []

    text = block.get("text", "")
    return [StreamChunk(content=text)] if text else []


__all__ = [
    "STREAMABLE_NODES",
    "StreamChunk",
    "StreamThinking",
    "StreamToolCall",
    "StreamToolResult",
    "StreamUsage",
    "StreamTraceUrl",
    "StreamEvent",
    "is_streamable_node",
    "has_tool_calls",
    "StreamEventProcessor",
]
