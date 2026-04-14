import os
from datetime import datetime
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, Template
from langfuse import Langfuse
from loguru import logger

from src.configs import SETTINGS


class PromptService:
    """Service for managing prompts with Langfuse + local file fallback."""

    def __init__(
        self,
        langfuse_client: Optional[Langfuse] = None,
        local_prompts_path: Optional[str] = None,
    ):
        self.langfuse = langfuse_client or Langfuse(public_key=SETTINGS.langfuse_public_key)
        self.local_prompts_path = local_prompts_path
        self._local_templates_cache: dict[str, str] = {}
        self._jinja_env: Optional[Environment] = None
        self._load_local_templates()

        if self.local_prompts_path and os.path.exists(self.local_prompts_path):
            self._jinja_env = Environment(
                loader=FileSystemLoader(self.local_prompts_path),
                autoescape=False,
            )

    def _load_local_templates(self):
        if self.local_prompts_path and os.path.exists(self.local_prompts_path):
            self._load_templates_from_directory(self.local_prompts_path)

    def _load_templates_from_directory(self, directory: str):
        """Load prompt templates from a directory, building dot-notation names from paths."""
        try:
            for root, _, files in os.walk(directory):
                for filename in files:
                    if filename.endswith(".md"):
                        filepath = os.path.join(root, filename)
                        relative_path = os.path.relpath(filepath, directory)
                        template_name = relative_path.replace(".md", "").replace(os.sep, ".")

                        try:
                            with open(filepath, encoding="utf-8") as f:
                                template_content = f.read()

                            if template_content.strip():
                                self._local_templates_cache[template_name] = template_content
                                logger.debug(f"Loaded template '{template_name}' from {filepath}")
                        except Exception as e:
                            logger.warning(f"Error reading template file {filepath}: {e}")
        except Exception as e:
            logger.warning(f"Error loading local templates from {directory}: {e}")

    def format_prompt(self, template_string: str, variables: Dict[str, Any] | None = None) -> str:
        """Format a Jinja2 template string with variables."""
        variables = variables or {}

        if "current_date" not in variables:
            variables["current_date"] = datetime.now().strftime("%Y-%m-%d")

        try:
            if self._jinja_env:
                template = self._jinja_env.from_string(template_string)
            else:
                template = Template(template_string)
            return template.render(**variables)
        except Exception as e:
            logger.error(f"Error formatting template: {e}")
            return template_string

    def get_prompt(
        self,
        prompt_name: str,
        variables: Dict[str, Any] | None = None,
        label: str | None = None,
        cache_ttl_seconds: int = 60,
        max_retries: int = 3,
        fetch_timeout_seconds: int = 3,
        use_local_only: bool = False,
        compile_template: bool = True,
    ) -> str | None:
        """Get a prompt template and format it with variables.

        Tries Langfuse first, falls back to local templates.
        """
        variables = variables or {}

        if not label:
            label = SETTINGS.env

        if not use_local_only:
            try:
                prompt_template = self.langfuse.get_prompt(
                    name=prompt_name,
                    label=label,
                    cache_ttl_seconds=cache_ttl_seconds,
                    fallback=None,
                    max_retries=max_retries,
                    fetch_timeout_seconds=fetch_timeout_seconds,
                )

                if prompt_template and compile_template:
                    return prompt_template.compile(**variables)
            except Exception as e:
                logger.warning(f"Failed to get prompt from Langfuse: {e}")

        return self._get_local_prompt(
            prompt_name=prompt_name,
            variables=variables,
            compile_template=compile_template,
        )

    def _get_local_prompt(
        self,
        prompt_name: str,
        variables: Dict[str, Any] | None = None,
        compile_template: bool = True,
    ) -> str | None:
        """Get prompt from local templates and format it."""
        variables = variables or {}
        template_string = self._local_templates_cache.get(prompt_name)
        if not template_string:
            return None

        if compile_template:
            return self.format_prompt(template_string, variables)
        return template_string


_prompt_service: Optional[PromptService] = None


def get_prompt_service(
    local_prompts_path: Optional[str] = None,
) -> PromptService:
    """Get the global prompt service instance (lazy singleton)."""
    global _prompt_service
    if _prompt_service is None:
        _prompt_service = PromptService(local_prompts_path=local_prompts_path)
    return _prompt_service
