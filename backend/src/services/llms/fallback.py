from langchain_core.language_models import BaseChatModel
from langfuse import Langfuse, observe
from langfuse.openai import OpenAI
from loguru import logger

from .exceptions import FallbackExceptionGroup
from .factory import create_langchain_model
from .schemas import ModelEntry


class FallbackOpenAIModel:
    def __init__(
        self,
        models: list[str | ModelEntry],
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        self.models = self._parse_models(models)
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.langfuse = Langfuse()

    def _parse_models(self, models: list[str | ModelEntry]) -> list[tuple[str, dict]]:
        parsed = []
        for model in models:
            if isinstance(model, str):
                parsed.append((model, {}))
            elif isinstance(model, ModelEntry):
                parsed.append((model.model, model.get_params()))
        return parsed

    @observe(name="completion")
    def completion(self, *args, **kwargs):
        exceptions: list[Exception] = []
        for model_name, default_params in self.models:
            try:
                merged_kwargs = {**default_params, **kwargs}
                response = self.client.chat.completions.create(model=model_name, *args, **merged_kwargs)
            except Exception as e:
                logger.error(f"Error calling model {model_name}: {e}")
                exceptions.append(e)
                continue
            return response

        raise FallbackExceptionGroup(exceptions)


class FallbackLangchainModel:
    """LangChain model wrapper with fallback support."""

    def __init__(
        self,
        models: list[str | BaseChatModel | ModelEntry],
        api_key: str | None = None,
        base_url: str | None = None,
        disable_streaming: bool = False,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = self._init_models(models, disable_streaming=disable_streaming)

    def _init_models(
        self,
        models: list[str | BaseChatModel | ModelEntry],
        disable_streaming: bool = False,
    ) -> BaseChatModel:
        _models = []
        for model in models:
            if isinstance(model, (str, ModelEntry)):
                _models.append(create_langchain_model(model, disable_streaming=disable_streaming))
            else:
                _models.append(model)

        if len(_models) > 1:
            return _models[0].with_fallbacks(_models[1:])

        return _models[0]

    def get_model(self) -> BaseChatModel:
        return self.model
