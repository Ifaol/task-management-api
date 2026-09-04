from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_user_repository
from app.modules.users.repository import UserRepository
from app.modules.users.schema import UserResponse, UserUpdate
from app.modules.users.service import (
    delete_user,
    get_user,
    get_users,
    update_user,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users_route(
    repository: UserRepository = Depends(get_user_repository),
) -> list[UserResponse]:
    return get_users(repository)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user_route(
    user_id: UUID,
    repository: UserRepository = Depends(get_user_repository),
) -> UserResponse:
    return get_user(user_id, repository)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user_route(
    user_id: UUID,
    user_update: UserUpdate,
    repository: UserRepository = Depends(get_user_repository),
) -> UserResponse:
    return update_user(user_id, user_update, repository)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_route(
    user_id: UUID,
    repository: UserRepository = Depends(get_user_repository),
) -> None:
    delete_user(user_id, repository)