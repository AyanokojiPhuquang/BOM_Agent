from fastapi import APIRouter, Depends, HTTPException, status

from src.app.auth import get_current_user
from src.app.dependencies import get_user_repository
from src.app.schemas.users import (
    CreateUserRequest,
    UpdateUserRequest,
    UserDetailResponse,
    UserListResponse,
)
from src.app.security import hash_password
from src.db.models.users import User
from src.db.repositories.user import UserRepository

router = APIRouter()


def _to_epoch_ms(dt) -> int:
    return int(dt.timestamp() * 1000)


def _user_to_detail(user: User) -> UserDetailResponse:
    return UserDetailResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role,
        is_active=user.is_active,
        created_at=_to_epoch_ms(user.created_at),
        updated_at=_to_epoch_ms(user.updated_at),
    )


@router.get("/users", response_model=UserListResponse)
async def list_users(
    repo: UserRepository = Depends(get_user_repository),
):
    users = await repo.list_all()
    total = await repo.count()
    return UserListResponse(
        items=[_user_to_detail(u) for u in users],
        total=total,
    )


@router.post("/users", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    repo: UserRepository = Depends(get_user_repository),
):
    existing = await repo.get_by_email(request.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    if request.role not in ("user", "admin"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be 'user' or 'admin'",
        )

    user = await repo.create(
        email=request.email,
        name=request.name,
        hashed_password=hash_password(request.password),
        role=request.role,
    )
    return _user_to_detail(user)


@router.get("/users/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: str,
    repo: UserRepository = Depends(get_user_repository),
):
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return _user_to_detail(user)


@router.put("/users/{user_id}", response_model=UserDetailResponse)
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    repo: UserRepository = Depends(get_user_repository),
):
    if request.role is not None and request.role not in ("user", "admin"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be 'user' or 'admin'",
        )

    if request.email is not None:
        existing = await repo.get_by_email(request.email)
        if existing and existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

    fields: dict = {}
    if request.name is not None:
        fields["name"] = request.name
    if request.email is not None:
        fields["email"] = request.email
    if request.role is not None:
        fields["role"] = request.role
    if request.is_active is not None:
        fields["is_active"] = request.is_active
    if request.password is not None:
        fields["hashed_password"] = hash_password(request.password)

    if not fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    user = await repo.update(user_id, **fields)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return _user_to_detail(user)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repository),
):
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )

    deleted = await repo.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
