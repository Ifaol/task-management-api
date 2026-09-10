from fastapi import APIRouter, BackgroundTasks, Depends, status

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
from app.services.email import send_welcome_email


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
    background_tasks: BackgroundTasks,
    repository: UserRepository = Depends(get_user_repository),
) -> RegisterResponse:
    response = register_user(
        user,
        repository,
    )

    background_tasks.add_task(
        send_welcome_email,
        user.email,
    )

    return response


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