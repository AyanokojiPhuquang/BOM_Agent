"""BOM assistant agent for Starlinks.

Uses a read-only agent with filesystem tools (grep/glob/read_file/ls)
to search optical transceiver datasheets, plus generate_bom.
"""

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from deepagents.backends import FilesystemBackend
from deepagents.graph import BASE_AGENT_PROMPT
from deepagents.middleware.patch_tool_calls import PatchToolCallsMiddleware
from deepagents.middleware.summarization import create_summarization_middleware
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langfuse import observe
from loguru import logger

from src.agents.middleware import ReadOnlyFilesystemMiddleware
from src.agents.registry import get_agent_definition, get_all_tools
from src.agents.schemas.context import BomAssistantContext
from src.agents.streaming import StreamEvent
from src.agents.utils import (
    finalize_invoke_trace,
    finalize_stream_trace,
    run_agent,
    setup_invoke_trace,
    setup_stream_trace,
    stream_agent_events,
)
from src.configs import SETTINGS
from src.services.llms.models import get_model
from src.services.prompts.service import get_prompt_service


def _build_agent(context: BomAssistantContext, checkpointer=None):
    """Build a read-only agent with filesystem access to product datasheets.

    Only exposes read tools (grep, glob, read_file, ls) and generate_bom.
    Write/edit/execute tools are excluded.

    Args:
        context: BomAssistantContext with session metadata
        checkpointer: Optional LangGraph checkpointer for conversation history

    Returns:
        Compiled LangGraph agent (CompiledStateGraph)
    """
    defn = get_agent_definition()
    model = get_model(defn.model)

    # Resolve prompt at build time
    prompt_service = get_prompt_service(local_prompts_path="configs/prompts")
    system_prompt = prompt_service.get_prompt(defn.prompt, use_local_only=True)
    final_system_prompt = system_prompt + "\n\n" + BASE_AGENT_PROMPT

    # Datasheets accessible via read-only grep/glob/read_file/ls
    datasheets_path = str(Path(SETTINGS.datasheets_dir).resolve())
    backend = FilesystemBackend(
        root_dir=datasheets_path,
        virtual_mode=True,
    )

    middleware = [
        ReadOnlyFilesystemMiddleware(backend=backend),
        create_summarization_middleware(model, backend),
        PatchToolCallsMiddleware(),
    ]

    return create_agent(
        model,
        system_prompt=final_system_prompt,
        tools=get_all_tools(),
        middleware=middleware,
        context_schema=BomAssistantContext,
        checkpointer=checkpointer,
        name="bom_assistant",
    ).with_config(
        {
            "recursion_limit": 1000,
            "metadata": {
                "ls_integration": "deepagents",
            },
        }
    )


def _initial_state(
    query: str,
    context: BomAssistantContext,
    image_urls: list[str] | None = None,
) -> dict:
    """Build the initial state for agent invocation."""
    if image_urls:
        content: list[dict] = [{"type": "text", "text": query}]
        for url in image_urls:
            content.append({"type": "image_url", "image_url": {"url": url}})
        messages = [HumanMessage(content=content)]
    else:
        messages = [HumanMessage(content=query)]

    return {
        "messages": messages,
    }


def _trace_input(query: str, context: BomAssistantContext) -> dict[str, Any]:
    """Build trace input for Langfuse."""
    return {
        "query": query,
        "knowledge_base_ids": context.knowledge_base_ids,
    }


@observe()
async def ainvoke(
    query: str,
    context: BomAssistantContext,
    checkpointer=None,
    image_urls: list[str] | None = None,
) -> dict[str, Any]:
    """Invoke the BOM assistant agent (non-streaming).

    Args:
        query: User's query
        context: BomAssistantContext
        checkpointer: Optional LangGraph checkpointer for conversation history
        image_urls: Optional list of image data URLs for multimodal input

    Returns:
        Dict with 'response', 'sources', and optionally 'trace_url'
    """
    setup_invoke_trace(
        session_id=context.session_id,
        user_id=context.user_id,
        input_data=_trace_input(query, context),
    )

    agent = _build_agent(context, checkpointer=checkpointer)
    result = await run_agent(
        agent,
        _initial_state(query, context, image_urls=image_urls),
        context=context,
        session_id=context.session_id,
        thread_id=context.conversation_id or "",
    )

    return finalize_invoke_trace(result)


@observe()
async def astream_events(
    query: str,
    context: BomAssistantContext,
    checkpointer=None,
    image_urls: list[str] | None = None,
) -> AsyncGenerator[StreamEvent, None]:
    """Stream typed events from the BOM assistant agent.

    Args:
        query: User's query
        context: BomAssistantContext
        checkpointer: Optional LangGraph checkpointer for conversation history
        image_urls: Optional list of image data URLs for multimodal input

    Yields:
        StreamEvent objects (StreamChunk, StreamToolCall, StreamToolResult, etc.)
    """
    setup_stream_trace(
        session_id=context.session_id,
        user_id=context.user_id,
        input_data=_trace_input(query, context),
    )

    agent = _build_agent(context, checkpointer=checkpointer)
    async for event in stream_agent_events(
        agent,
        _initial_state(query, context, image_urls=image_urls),
        context=context,
        session_id=context.session_id,
        thread_id=context.conversation_id or "",
    ):
        yield event

    finalize_stream_trace()
