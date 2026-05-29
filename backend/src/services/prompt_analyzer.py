"""Prompt Analyzer Service.

Uses an LLM to intelligently integrate or remove user instructions
from the base system prompt without breaking its structure.
"""

from loguru import logger

from src.services.llms.models import get_model
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel


class AnalyzerOutput(BaseModel):
    """Output from the prompt analyzer."""
    updated_prompt: str


ANALYZER_SYSTEM_PROMPT = """You are a System Prompt Editor. Your ONLY job is to add or remove lines in the "## User Custom Instructions" section at the END of the system prompt.

CRITICAL RULES:
1. NEVER modify ANY text outside the "## User Custom Instructions" section.
2. NEVER replace words, fix grammar, or "improve" the existing prompt content.
3. When ADDING: If "## User Custom Instructions" section exists, append the new instruction as a bullet point. If it doesn't exist, add the section at the very end.
4. When REMOVING: Find and remove only the specific bullet point. If the section becomes empty, remove the section header too.
5. Output the COMPLETE system prompt - every single character of the original must be preserved except for the User Custom Instructions section changes.
6. DO NOT paraphrase, rewrite, or restructure any part of the original prompt.

FORMAT for instructions in the section:
## User Custom Instructions

- First instruction here
- Second instruction here
"""


async def analyze_and_update_prompt(
    current_prompt: str,
    action: str,  # "ADD" or "DELETE"
    instruction: str,
) -> str:
    """Add or remove an instruction from the User Custom Instructions section.

    Uses simple string manipulation (reliable) instead of LLM (unpredictable).
    """
    section_header = "## User Custom Instructions"
    bullet = f"- {instruction}"

    if action == "ADD":
        if section_header in current_prompt:
            # Append to existing section
            return current_prompt.rstrip() + f"\n{bullet}\n"
        else:
            # Create new section at the end
            return current_prompt.rstrip() + f"\n\n{section_header}\n\n{bullet}\n"

    elif action == "DELETE":
        # Remove the bullet line
        lines = current_prompt.split("\n")
        new_lines = [l for l in lines if l.strip() != bullet.strip() and l.strip() != instruction.strip()]

        result = "\n".join(new_lines)

        # If section is now empty (only header, no bullets), remove it
        if section_header in result:
            section_start = result.index(section_header)
            after_header = result[section_start + len(section_header):].strip()
            if not after_header or not after_header.startswith("-"):
                result = result[:section_start].rstrip() + "\n"

        return result

    return current_prompt
