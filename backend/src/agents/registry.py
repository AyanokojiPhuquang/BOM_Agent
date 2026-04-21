"""Agent registry.

Central definition of each agent type — its prompt, model,
and the custom tools it is allowed to use.
"""

from dataclasses import dataclass, field

from src.agents.tools.escalate_to_human import escalate_to_human
from src.agents.tools.generate_bom import generate_bom
from src.agents.tools.inventory_checker import check_product_inventory
from src.agents.tools.product_search import search_products, get_product_detail


@dataclass(frozen=True)
class AgentDefinition:
    """Static definition of an agent type."""

    prompt: str
    """Prompt name in dot-notation, matching local template path."""

    model: str
    """Model group name from configs/model_config.yaml."""

    tools: list = field(default_factory=list)
    """Custom tool callables this agent is allowed to use."""


AGENT_REGISTRY: dict[str, AgentDefinition] = {
    "bom_assistant": AgentDefinition(
        prompt="agents.bom_assistant",
        model="agents/bom_assistant/default",
        tools=[search_products, get_product_detail, generate_bom, escalate_to_human, check_product_inventory],
    ),
}

DEFAULT_AGENT = AGENT_REGISTRY["bom_assistant"]


def get_agent_definition(agent_type: str = "bom_assistant") -> AgentDefinition:
    """Look up the agent definition for a given type."""
    return AGENT_REGISTRY.get(agent_type, DEFAULT_AGENT)


def get_all_tools() -> list:
    """Collect the union of all custom tools across all registered agents."""
    seen = set()
    tools = []
    for defn in AGENT_REGISTRY.values():
        for tool in defn.tools:
            if id(tool) not in seen:
                seen.add(id(tool))
                tools.append(tool)
    return tools
