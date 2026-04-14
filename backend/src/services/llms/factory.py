"""Model factory for creating LangChain models.

Supports OpenAI-compatible models. Gemini support can be added later.
"""

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from src.configs import SETTINGS

from .schemas import ModelEntry


def create_langchain_model(
    model: str | ModelEntry,
    disable_streaming: bool = False,
) -> BaseChatModel:
    """Factory function to create appropriate LangChain model based on provider.

    Args:
        model: Model name string or ModelEntry with configuration
        disable_streaming: Whether to disable streaming

    Returns:
        BaseChatModel instance
    """
    if isinstance(model, str):
        model_name = model
        params = {}
        explicit_provider = None
    else:
        model_name = model.model
        params = model.get_params()
        explicit_provider = model.provider

    provider = _resolve_provider(model_name, explicit_provider)

    if provider == "gemini":
        raise NotImplementedError("Gemini provider not yet configured. Add langchain-google-genai to enable.")

    return _create_openai_model(model_name, params, disable_streaming)


def _resolve_provider(model_name: str, explicit_provider: str | None) -> str:
    if explicit_provider:
        return explicit_provider
    if model_name.startswith("gemini/"):
        return "gemini"
    return "openai"


def _create_openai_model(
    model_name: str,
    params: dict,
    disable_streaming: bool,
) -> ChatOpenAI:
    # When reasoning_effort is set, use the Responses API `reasoning` dict
    # so that reasoning summaries are streamed back to the client.
    reasoning_effort = params.pop("reasoning_effort", None)
    kwargs: dict = {}
    if reasoning_effort:
        kwargs["reasoning"] = {"effort": reasoning_effort, "summary": "auto"}
        kwargs["use_responses_api"] = True
        kwargs["output_version"] = "responses/v1"

    return ChatOpenAI(
        model_name=model_name,
        api_key=SETTINGS.openai_api_key,
        base_url=SETTINGS.openai_api_base_url,
        disable_streaming=disable_streaming,
        **kwargs,
        **params,
    )
