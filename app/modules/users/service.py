from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schema import UserResponse, UserUpdate


def create_user(
    email: str,
    hashed_password: str,
    repository: UserRepository,
) -> UserResponse:
    existing_user = repository.get_by_email(email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    new_user = User(
        id=uuid4(),
        email=email,
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )

    created_user = repository.create(new_user)

    return UserResponse.model_validate(created_user)


def get_users(repository: UserRepository) -> list[UserResponse]:
    users = repository.get_all()

    return [
        UserResponse.model_validate(user)
        for user in users
    ]


def get_user(
    user_id: UUID,
    repository: UserRepository,
) -> UserResponse:
    user = repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse.model_validate(user)


def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    repository: UserRepository,
) -> UserResponse:
    user = repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_data = user_update.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_user = repository.get_by_email(
            update_data["email"],
        )

        if existing_user is not None and existing_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

    for field, value in update_data.items():
        setattr(user, field, value)

    updated_user = repository.update(user)

    return UserResponse.model_validate(updated_user)


def delete_user(
    user_id: UUID,
    repository: UserRepository,
) -> None:
    user = repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    repository.delete(user_id)