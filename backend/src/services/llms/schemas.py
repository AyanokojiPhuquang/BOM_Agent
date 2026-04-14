from typing import Literal

from pydantic import BaseModel, Field


class ModelEntry(BaseModel):
    """Individual model configuration with optional parameters."""

    model: str

    provider: Literal["openai", "gemini"] | None = None

    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, gt=0)
    top_p: float | None = Field(default=None, ge=0.0, le=1.0)
    frequency_penalty: float | None = Field(default=None, ge=-2.0, le=2.0)
    presence_penalty: float | None = Field(default=None, ge=-2.0, le=2.0)
    timeout: int | None = Field(default=None, gt=0)
    reasoning_effort: Literal["low", "medium", "high"] | None = Field(default=None)

    def get_params(self) -> dict:
        """Get parameters as dict, excluding model name and None values."""
        return {k: v for k, v in self.model_dump().items() if k not in ("model", "provider") and v is not None}


class ModelConfig(BaseModel):
    model_type: Literal["openai", "langchain"]
    primary: str | ModelEntry
    fallback: list[str | ModelEntry] = []
