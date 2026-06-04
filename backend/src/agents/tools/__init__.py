"""Custom tools for the BOM assistant agent.

Built-in DeepAgent tools (grep/glob/read_file/ls) are provided
automatically by the filesystem backend and not listed here.
"""

from src.agents.tools.escalate_to_human import escalate_to_human
from src.agents.tools.generate_bom import generate_bom
from src.agents.tools.get_datasheet import get_datasheet_link

__all__ = [
    "all_tools",
    "escalate_to_human",
    "generate_bom",
    "get_datasheet_link",
    "get_tools",
]

# Custom tools — registered with the agent alongside DeepAgent built-ins.
all_tools = [
    generate_bom,
    escalate_to_human,
    get_datasheet_link,
]


def get_tools() -> list:
    """Return all custom tools for the BOM assistant agent."""
    return list(all_tools)
