import logging
from pathlib import Path
from typing import Type, TypeVar

import yaml
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse.langchain import CallbackHandler
from pydantic import BaseModel

from src.configs import SETTINGS

from .fallback import FallbackLangchainModel, FallbackOpenAIModel
from .schemas import ModelConfig

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class ModelRegistry:
    def __init__(self, config_path: str = "configs/model_config.yaml"):
        self.config_path = Path(config_path)
        self.model_groups: dict[str, ModelConfig] = {}
        self.models: dict[str, FallbackOpenAIModel | FallbackLangchainModel] = {}
        self._load_config()
        self._init_models()

    def _load_config(self):
        """Load model configuration from YAML file."""
        try:
            with open(self.config_path) as f:
                config = yaml.safe_load(f)

            models_config = config.get("models", {})
            for group_name, group_config in models_config.items():
                model_config = ModelConfig(**group_config)
                self.model_groups[group_name] = model_config

            logger.info(f"Loaded {len(self.model_groups)} model groups")

        except Exception as e:
            logger.error(f"Failed to load model config: {e}")
            raise

    def _init_models(self):
        """Initialize fallback models based on model type."""
        try:
            for group_name, config in self.model_groups.items():
                models = [config.primary, *config.fallback]

                if config.model_type == "openai":
                    self.models[group_name] = FallbackOpenAIModel(
                        models=models,
                        api_key=SETTINGS.openai_api_key,
                        base_url=SETTINGS.openai_api_base_url,
                    )
                elif config.model_type == "langchain":
                    self.models[group_name] = FallbackLangchainModel(
                        models=models,
                        api_key=SETTINGS.openai_api_key,
                        base_url=SETTINGS.openai_api_base_url,
                        disable_streaming=False,
                    ).get_model()
                else:
                    logger.warning(f"Unknown model type '{config.model_type}' for group '{group_name}'")

            logger.info(f"Initialized {len(self.models)} fallback models")

        except Exception as e:
            logger.error(f"Failed to initialize fallback models: {e}")
            raise

    def get_model(self, group_name: str) -> FallbackOpenAIModel | FallbackLangchainModel:
        return self.models[group_name]


MODEL_REGISTRY = ModelRegistry()


def get_model(group_name: str) -> FallbackOpenAIModel | FallbackLangchainModel:
    """Get model instance for a specific group."""
    if group_name not in MODEL_REGISTRY.models:
        raise ValueError(f"Model group '{group_name}' not found")
    return MODEL_REGISTRY.get_model(group_name)


async def llm_invoke(
    model_name: str,
    schema: Type[T],
    user_prompt: str,
    system_prompt: str | None = None,
) -> T:
    """Invoke LLM with structured output and Langfuse tracking.

    Args:
        model_name: Model group name from config
        schema: Pydantic model class for structured output
        user_prompt: User message content
        system_prompt: Optional system message content

    Returns:
        Validated Pydantic model instance
    """
    llm = get_model(model_name)
    structured_llm = llm.with_structured_output(schema)

    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=user_prompt))

    langfuse_handler = CallbackHandler()
    result = await structured_llm.ainvoke(messages, config={"callbacks": [langfuse_handler]})

    return result
