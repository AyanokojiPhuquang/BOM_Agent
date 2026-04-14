"""Starlink agents module.

This module provides a BOM assistant agent built with LangChain + LangGraph
for optical transceiver recommendation and quotation.

Exports:
    ainvoke: Non-streaming agent invocation
    astream_events: Streaming agent invocation (typed events)
    BomAssistantContext: Context schema for the agent
"""

from src.agents.agent import ainvoke, astream_events
from src.agents.schemas.context import BomAssistantContext

__all__ = [
    "ainvoke",
    "astream_events",
    "BomAssistantContext",
]
