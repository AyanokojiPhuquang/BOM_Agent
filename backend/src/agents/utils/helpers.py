"""Shared utility functions for the BOM assistant agent.

Extracts common patterns: message building, LLM invocation, and graph orchestration.
Includes Langfuse tracing integration.
"""

from collections.abc import AsyncGenerator
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from loguru import logger

from src.agents.streaming import (
    StreamChunk,
    StreamEvent,
    StreamEventProcessor,
)


# --- Message helpers ---


def build_messages(query: str, conversation_history: list[dict] | None = None) -> list[BaseMessage]:
    """Convert dict history + query into LangChain messages."""
    messages: list[BaseMessage] = []
    if conversation_history:
        for msg in conversation_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))
    messages.append(HumanMessage(content=query))
    return messages


def extract_ai_response(messages: list[BaseMessage]) -> str:
    """Get last AIMessage content."""
    ai_messages = [m for m in messages if isinstance(m, AIMessage)]
    return ai_messages[-1].content if ai_messages else ""


# --- Agent orchestration helpers ---


def _build_run_config(session_id: str = "", thread_id: str = "") -> dict:
    """Build LangGraph run config with Langfuse callback and optional thread_id.

    Args:
        session_id: Used for Langfuse tracing session. Falls back as thread_id if thread_id not set.
        thread_id: Used for LangGraph checkpointer thread. Typically the conversation_id.
    """
    config: dict[str, Any] = {"callbacks": [CallbackHandler()]}
    effective_thread_id = thread_id or session_id
    if effective_thread_id:
        config.setdefault("configurable", {})["thread_id"] = effective_thread_id
    return config


def make_graph(state_type, node_fn, node_name: str):
    """Build a single-node StateGraph: START -> node -> END."""
    graph = StateGraph(state_type)
    graph.add_node(node_name, node_fn)
    graph.add_edge(START, node_name)
    graph.add_edge(node_name, END)
    return graph.compile()


async def run_agent(
    graph,
    initial_state: dict,
    *,
    context: Any | None = None,
    session_id: str = "",
    thread_id: str = "",
) -> dict[str, Any]:
    """Invoke graph, return {response, sources}."""
    config = _build_run_config(session_id, thread_id=thread_id)

    try:
        result = await graph.ainvoke(
            initial_state,
            config=config,
            context=context,
        )
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise

    return {
        "response": extract_ai_response(result["messages"]),
        "sources": result.get("sources", []),
    }


async def stream_agent_events(
    graph,
    initial_state: dict,
    *,
    context: Any | None = None,
    session_id: str = "",
    thread_id: str = "",
) -> AsyncGenerator[StreamEvent, None]:
    """Stream typed events from graph with error handling."""
    config = _build_run_config(session_id, thread_id=thread_id)
    processor = StreamEventProcessor()

    try:
        async for msg, metadata in graph.astream(
            initial_state,
            config=config,
            stream_mode="messages",
            context=context,
        ):
            node_name = metadata.get("langgraph_node", "")
            result = processor.process_message(msg, node_name)
            if result:
                if isinstance(result, list):
                    for event in result:
                        yield event
                else:
                    yield result
    except Exception as e:
        logger.error(f"Agent streaming error: {e}")
        yield StreamChunk(content=f"Error: {e}")


# --- Langfuse tracing helpers ---

AGENT_NAME = "bom-assistant-agent"


def setup_invoke_trace(
    *,
    session_id: str,
    user_id: str,
    input_data: dict,
) -> None:
    """Set up Langfuse trace for a non-streaming invocation."""
    langfuse = get_client()
    langfuse.update_current_trace(
        name=AGENT_NAME,
        session_id=session_id,
        user_id=user_id,
        input=input_data,
    )


def finalize_invoke_trace(result: dict) -> dict:
    """Attach trace URL and output to the current trace."""
    langfuse = get_client()
    trace_url = langfuse.get_trace_url()
    if trace_url:
        result["trace_url"] = trace_url
    langfuse.update_current_trace(output={"response": result.get("response", "")})
    return result


def setup_stream_trace(
    *,
    session_id: str,
    user_id: str,
    input_data: dict,
) -> None:
    """Set up Langfuse trace for streaming."""
    langfuse = get_client()
    langfuse.update_current_trace(
        name=AGENT_NAME,
        session_id=session_id,
        user_id=user_id,
        input=input_data,
    )


def finalize_stream_trace() -> str | None:
    """Finalize trace and return URL."""
    langfuse = get_client()
    trace_url = langfuse.get_trace_url()
    logger.info(f"Trace URL: {trace_url}")
    return trace_url
