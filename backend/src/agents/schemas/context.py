"""Context schema for the BOM assistant agent.

Defines the runtime context passed to the agent on every invocation.
"""

from typing import Any

from pydantic import BaseModel, Field


class BomAssistantContext(BaseModel):
    """Context for the BOM assistant agent.

    Carries session metadata needed by the agent, middleware, and tools.
    """

    # Core identifiers
    session_id: str
    user_id: str
    user_email: str | None = None
    conversation_id: str | None = None

    # Optional configuration
    knowledge_base_ids: list[str] = Field(default_factory=list)
    output_format: str | None = None

    def model_dump(self, **kwargs) -> dict[str, Any]:
        """Convert to dict, excluding None values."""
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}
