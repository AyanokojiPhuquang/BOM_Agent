from fastapi import APIRouter, Depends, HTTPException, status

from src.app.auth import get_current_user
from src.app.dependencies import get_user_repository
from src.app.schemas.auth import LoginRequest, LoginResponse, UserResponse
from src.app.security import create_access_token, verify_password
from src.db.models.users import User
from src.db.repositories.user import UserRepository

router = APIRouter()


@router.post("/auth/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    repo: UserRepository = Depends(get_user_repository),
):
    user = await repo.get_by_email(request.email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(subject=user.id)
    return LoginResponse(
        user=UserResponse(id=user.id, email=user.email, name=user.name, role=user.role),
        token=token,
    )


@router.post("/auth/logout")
async def logout():
    return {"message": "Logged out"}


@router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
    )
