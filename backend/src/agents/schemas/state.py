"""State schema for the BOM assistant agent.

Defines the state that flows through the LangGraph agent graph.
"""

from typing import Any

from langgraph.graph import MessagesState


class BomAssistantState(MessagesState):
    """State for the BOM assistant agent.

    Extends MessagesState from LangGraph with a sources list
    for tracking retrieved knowledge base entries.
    """

    sources: list[dict[str, Any]] = []
