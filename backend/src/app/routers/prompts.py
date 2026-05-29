"""Prompt management router.

Supports viewing prompts and managing user behavioral instructions
that get integrated into the system prompt via an Analyzer LLM.
"""

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.app.auth import get_current_user
from src.db.models.users import User

router = APIRouter(prefix="/prompts", tags=["prompts"])

PROMPTS_DIR = Path("configs/prompts")
PROMPTS_BACKUP_DIR = Path("configs/prompts_original")
USER_INSTRUCTIONS_FILE = Path("data/user_instructions.json")


# --- Schemas ---


class UserInstruction(BaseModel):
    id: str
    content: str


class UserInstructionsResponse(BaseModel):
    instructions: list[UserInstruction]
    is_processing: bool = False


class AddInstructionRequest(BaseModel):
    content: str


class AddInstructionResponse(BaseModel):
    instruction: UserInstruction
    message: str


# --- Helpers ---


def _ensure_backups():
    """Create backup of original prompts if not already done."""
    if not PROMPTS_DIR.exists():
        return
    if not PROMPTS_BACKUP_DIR.exists():
        import shutil
        shutil.copytree(PROMPTS_DIR, PROMPTS_BACKUP_DIR)


def _load_instructions() -> list[dict]:
    """Load user instructions from file."""
    if USER_INSTRUCTIONS_FILE.exists():
        return json.loads(USER_INSTRUCTIONS_FILE.read_text(encoding="utf-8"))
    return []


def _save_instructions(instructions: list[dict]):
    """Save user instructions to file."""
    USER_INSTRUCTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USER_INSTRUCTIONS_FILE.write_text(
        json.dumps(instructions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _get_main_prompt_path() -> Path:
    """Get the path to the main BOM assistant prompt."""
    return PROMPTS_DIR / "agents" / "bom_assistant.md"


# Create backups on module load
_ensure_backups()


# --- Endpoints ---


@router.get("/instructions", response_model=UserInstructionsResponse)
async def list_instructions(current_user: User = Depends(get_current_user)):
    """List all active user instructions."""
    instructions = _load_instructions()
    return UserInstructionsResponse(
        instructions=[UserInstruction(**i) for i in instructions],
    )


@router.post("/instructions", response_model=AddInstructionResponse)
async def add_instruction(
    request: AddInstructionRequest,
    current_user: User = Depends(get_current_user),
):
    """Add a new behavioral instruction. The Analyzer LLM integrates it into the system prompt."""
    from src.services.prompt_analyzer import analyze_and_update_prompt
    import uuid

    if not request.content.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Instruction cannot be empty")

    # Load current prompt
    prompt_path = _get_main_prompt_path()
    if not prompt_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="System prompt not found")

    current_prompt = prompt_path.read_text(encoding="utf-8")

    # Use Analyzer LLM to integrate instruction
    updated_prompt = await analyze_and_update_prompt(
        current_prompt=current_prompt,
        action="ADD",
        instruction=request.content.strip(),
    )

    # Save updated prompt
    prompt_path.write_text(updated_prompt, encoding="utf-8")

    # Invalidate prompt cache so changes take effect immediately
    from src.services.prompts.service import invalidate_prompt_cache
    invalidate_prompt_cache()

    # Save instruction to list
    instruction_id = str(uuid.uuid4())[:8]
    instructions = _load_instructions()
    instructions.append({"id": instruction_id, "content": request.content.strip()})
    _save_instructions(instructions)

    return AddInstructionResponse(
        instruction=UserInstruction(id=instruction_id, content=request.content.strip()),
        message="Instruction added successfully",
    )


@router.delete("/instructions/{instruction_id}")
async def delete_instruction(
    instruction_id: str,
    current_user: User = Depends(get_current_user),
):
    """Remove a behavioral instruction. The Analyzer LLM removes it from the system prompt."""
    from src.services.prompt_analyzer import analyze_and_update_prompt

    instructions = _load_instructions()
    target = next((i for i in instructions if i["id"] == instruction_id), None)

    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instruction not found")

    # Load current prompt
    prompt_path = _get_main_prompt_path()
    current_prompt = prompt_path.read_text(encoding="utf-8")

    # Use Analyzer LLM to remove instruction
    updated_prompt = await analyze_and_update_prompt(
        current_prompt=current_prompt,
        action="DELETE",
        instruction=target["content"],
    )

    # Save updated prompt
    prompt_path.write_text(updated_prompt, encoding="utf-8")

    # Invalidate prompt cache
    from src.services.prompts.service import invalidate_prompt_cache
    invalidate_prompt_cache()

    # Remove from list
    instructions = [i for i in instructions if i["id"] != instruction_id]
    _save_instructions(instructions)

    return {"message": "Instruction removed successfully"}


@router.post("/reset")
async def reset_prompt(current_user: User = Depends(get_current_user)):
    """Reset the system prompt to its original version and clear all instructions."""
    prompt_path = _get_main_prompt_path()
    backup_path = PROMPTS_BACKUP_DIR / "agents" / "bom_assistant.md"

    if not backup_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No backup found")

    # Restore original
    original = backup_path.read_text(encoding="utf-8")
    prompt_path.write_text(original, encoding="utf-8")

    # Invalidate prompt cache
    from src.services.prompts.service import invalidate_prompt_cache
    invalidate_prompt_cache()

    # Clear instructions
    _save_instructions([])

    return {"message": "System prompt reset to original"}
