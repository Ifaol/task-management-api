from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_user_repository
from app.modules.auth.schema import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from app.modules.auth.service import (
    login_user,
    register_user,
)
from app.modules.users.repository import UserRepository


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_route(
    user: RegisterRequest,
    repository: UserRepository = Depends(get_user_repository),
) -> RegisterResponse:
    return register_user(
        user,
        repository,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_route(
    credentials: LoginRequest,
    repository: UserRepository = Depends(get_user_repository),
) -> TokenResponse:
    return login_user(
        credentials,
        repository,
    )