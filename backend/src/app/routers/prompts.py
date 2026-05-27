"""Prompt management router.

Allows viewing and editing agent prompts via the UI.
"""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.app.auth import get_current_user
from src.db.models.users import User

router = APIRouter(prefix="/prompts", tags=["prompts"])

PROMPTS_DIR = Path("configs/prompts")


class PromptItem(BaseModel):
    path: str
    name: str
    category: str
    content: str


class PromptListResponse(BaseModel):
    prompts: list[PromptItem]


class UpdatePromptRequest(BaseModel):
    content: str


@router.get("/", response_model=PromptListResponse)
async def list_prompts(current_user: User = Depends(get_current_user)):
    """List all available prompts."""
    prompts = []
    if PROMPTS_DIR.exists():
        for md_file in sorted(PROMPTS_DIR.rglob("*.md")):
            relative = md_file.relative_to(PROMPTS_DIR)
            parts = relative.parts
            category = parts[0] if len(parts) > 1 else "general"
            prompts.append(PromptItem(
                path=str(relative),
                name=md_file.stem,
                category=category,
                content=md_file.read_text(encoding="utf-8"),
            ))
    return PromptListResponse(prompts=prompts)


@router.get("/{prompt_path:path}", response_model=PromptItem)
async def get_prompt(prompt_path: str, current_user: User = Depends(get_current_user)):
    """Get a specific prompt by path."""
    file_path = PROMPTS_DIR / prompt_path
    if not file_path.exists() or not file_path.suffix == ".md":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")

    relative = file_path.relative_to(PROMPTS_DIR)
    parts = relative.parts
    category = parts[0] if len(parts) > 1 else "general"

    return PromptItem(
        path=str(relative),
        name=file_path.stem,
        category=category,
        content=file_path.read_text(encoding="utf-8"),
    )


@router.put("/{prompt_path:path}", response_model=PromptItem)
async def update_prompt(
    prompt_path: str,
    request: UpdatePromptRequest,
    current_user: User = Depends(get_current_user),
):
    """Update a prompt's content."""
    if ".." in prompt_path:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid path")

    file_path = PROMPTS_DIR / prompt_path
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")

    file_path.write_text(request.content, encoding="utf-8")

    relative = file_path.relative_to(PROMPTS_DIR)
    parts = relative.parts
    category = parts[0] if len(parts) > 1 else "general"

    return PromptItem(
        path=str(relative),
        name=file_path.stem,
        category=category,
        content=request.content,
    )
