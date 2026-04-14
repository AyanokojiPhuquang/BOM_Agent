"""Interactive CLI REPL for testing the Starlink BOM assistant agent.

Usage:
    uv run python scripts/cli/cli.py [options]

Examples:
    uv run python scripts/cli/cli.py                  # streaming (default)
    uv run python scripts/cli/cli.py --no-stream      # non-streaming
    uv run python scripts/cli/cli.py -v               # verbose logging
"""

import argparse
import asyncio
import sys
import uuid

from loguru import logger as _logger

from scripts.cli.colors import C
from scripts.cli.repl import handle_command, print_banner, read_user_input

# Import configs first to ensure environment variables are set
import src.configs  # noqa: F401

# Configure logging AFTER imports to suppress eager loguru output.
_logger.remove()
_logger.add(sys.stderr, level="WARNING")


# -- Arg parsing --------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interactive CLI for the Starlink BOM assistant agent",
    )
    parser.add_argument(
        "--no-stream",
        action="store_true",
        default=False,
        help="Use ainvoke() instead of astream_events()",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Show full loguru DEBUG logs (default: WARNING only)",
    )
    return parser.parse_args()


def configure_logging(verbose: bool) -> None:
    if verbose:
        _logger.remove()
        _logger.add(sys.stderr, level="DEBUG")


# -- Token usage display ------------------------------------------------------


def print_usage_summary(usage) -> None:
    """Print token usage breakdown in gray."""
    total = usage.input_tokens + usage.output_tokens
    if total == 0:
        return

    u, r = C.USAGE, C.RESET
    print()
    print(f"{u}  {'─' * 44}")
    print("  Token Usage:")
    print(f"    Input tokens:          {usage.input_tokens:>8,}")
    if usage.cache_read_tokens:
        print(f"      Cache read:          {usage.cache_read_tokens:>8,}")
    if usage.cache_creation_tokens:
        print(f"      Cache creation:      {usage.cache_creation_tokens:>8,}")
    print(f"    Output tokens:         {usage.output_tokens:>8,}")
    if usage.reasoning_tokens:
        print(f"      Reasoning:           {usage.reasoning_tokens:>8,}")
        print(f"      Response:            {usage.output_tokens - usage.reasoning_tokens:>8,}")
    print(f"    Total:                 {total:>8,}")
    print(f"  {'─' * 44}{r}")


# -- Stream printer -----------------------------------------------------------


class StreamPrinter:
    """Manages streaming output state for incremental printing."""

    def __init__(self):
        self._streaming_text = False
        self._streaming_thinking = False
        self.total_usage = None

    def end_block(self) -> None:
        """Close any open streaming block."""
        if self._streaming_thinking:
            print(C.RESET)
            self._streaming_thinking = False
        if self._streaming_text:
            print(C.RESET)
            self._streaming_text = False

    def print_thinking(self, content: str) -> None:
        """Print a thinking/reasoning chunk."""
        if self._streaming_text:
            print(C.RESET)
            self._streaming_text = False
        if not self._streaming_thinking:
            print(f"  {C.THINKING}[thinking] ", end="", flush=True)
            self._streaming_thinking = True
        print(content, end="", flush=True)

    def print_chunk(self, content: str) -> None:
        """Print a text content chunk."""
        if self._streaming_thinking:
            print(C.RESET)
            self._streaming_thinking = False
        if not self._streaming_text:
            print(f"{C.AGENT}Agent: {C.RESET}{C.GREEN}", end="", flush=True)
            self._streaming_text = True
        print(content, end="", flush=True)

    def print_tool_call(self, name: str, args: dict) -> None:
        """Print a tool call line."""
        self.end_block()
        args_str = ", ".join(f"{k}={v!r}" for k, v in args.items())
        print(f"  {C.TOOL_CALL}-> {name}({args_str}){C.RESET}")

    def print_tool_result(self, name: str, content: str, status: str) -> None:
        """Print a tool result line."""
        self.end_block()
        preview = content[:200] + ("..." if len(content) > 200 else "")
        status_color = C.GREEN if status in ("ok", "success") else C.RED
        print(f"  {C.TOOL_RESULT}<- {name} ({status_color}{status}{C.TOOL_RESULT}): {C.DIM}{preview}{C.RESET}")

    def accumulate_usage(self, usage) -> None:
        """Accumulate token usage from a StreamUsage event."""
        from src.agents.streaming import StreamUsage

        if self.total_usage is None:
            self.total_usage = StreamUsage()
        self.total_usage.input_tokens += usage.input_tokens
        self.total_usage.output_tokens += usage.output_tokens
        self.total_usage.reasoning_tokens += usage.reasoning_tokens
        self.total_usage.cache_read_tokens += usage.cache_read_tokens
        self.total_usage.cache_creation_tokens += usage.cache_creation_tokens


# -- Response handlers --------------------------------------------------------


async def handle_stream_response(
    query: str,
    context,
) -> str:
    """Stream events and return the accumulated assistant text."""
    from src.agents import astream_events
    from src.agents.streaming import (
        StreamChunk,
        StreamThinking,
        StreamToolCall,
        StreamToolResult,
        StreamUsage,
    )

    printer = StreamPrinter()
    accumulated = []

    try:
        async for event in astream_events(query=query, context=context):
            if isinstance(event, StreamToolCall):
                printer.print_tool_call(event.name, event.args)
            elif isinstance(event, StreamToolResult):
                printer.print_tool_result(event.name, event.content, event.status)
            elif isinstance(event, StreamUsage):
                printer.accumulate_usage(event)
            elif isinstance(event, StreamThinking):
                printer.print_thinking(event.content)
            elif isinstance(event, StreamChunk):
                printer.print_chunk(event.content)
                accumulated.append(event.content)
    except KeyboardInterrupt:
        print(f"{C.RESET}\n  {C.YELLOW}[interrupted]{C.RESET}")

    printer.end_block()
    if printer.total_usage:
        print_usage_summary(printer.total_usage)

    return "".join(accumulated)


async def handle_invoke_response(
    query: str,
    context,
) -> str:
    """Call ainvoke() and return the response text."""
    from src.agents import ainvoke

    print(f"{C.AGENT}Agent: {C.RESET}{C.GREEN}", end="", flush=True)
    try:
        result = await ainvoke(query=query, context=context)
        response = result.get("response", "")
        print(f"{response}{C.RESET}")

        sources = result.get("sources", [])
        if sources:
            print(f"  {C.CYAN}[sources: {len(sources)} items]")
            for s in sources[:5]:
                print(f"    - {s}")
            print(C.RESET, end="")

        return response
    except KeyboardInterrupt:
        print(f"{C.RESET}\n  {C.YELLOW}[interrupted]{C.RESET}")
        return ""


# -- Main loop ----------------------------------------------------------------


async def main_loop(args: argparse.Namespace) -> None:
    configure_logging(args.verbose)

    streaming = not args.no_stream
    session_id = str(uuid.uuid4())

    def on_new_session(state: dict) -> None:
        state["session_id"] = str(uuid.uuid4())
        print(f"  New session: {state['session_id']}")

    print_banner(
        "Starlinks BOM Assistant — Interactive CLI",
        streaming=streaming,
        extra_lines=[f"  Session:     {C.DIM}{session_id}{C.RESET}"],
    )

    state = {
        "running": True,
        "session_id": session_id,
        "on_new_session": on_new_session,
    }

    while state["running"]:
        user_input = read_user_input()
        if user_input is None:
            break

        user_input = user_input.strip()
        if not user_input:
            continue

        if handle_command(user_input, state):
            if not state["running"]:
                break
            continue

        from src.agents import BomAssistantContext

        context = BomAssistantContext(
            session_id=state["session_id"],
            user_id="cli",
        )

        try:
            if streaming:
                await handle_stream_response(user_input, context)
            else:
                await handle_invoke_response(user_input, context)
        except Exception as e:
            print(f"\n  {C.ERROR}[error: {e}]{C.RESET}")

    print(f"{C.DIM}Goodbye!{C.RESET}")


if __name__ == "__main__":
    asyncio.run(main_loop(parse_args()))
