from typing import Optional

from pydantic import BaseModel, EmailStr

from src.app.schemas.auth import UserResponse


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str = "user"


class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserDetailResponse(UserResponse):
    is_active: bool
    created_at: int
    updated_at: int


class UserListResponse(BaseModel):
    items: list[UserDetailResponse]
    total: int
