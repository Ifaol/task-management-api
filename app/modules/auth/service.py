from fastapi import HTTPException, status
from pwdlib import PasswordHash

from app.core.security import create_access_token
from app.modules.auth.schema import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from app.modules.users.repository import UserRepository
from app.modules.users.service import create_user


password_hash = PasswordHash.recommended()


def register_user(
    user: RegisterRequest,
    repository: UserRepository,
) -> RegisterResponse:
    hashed_password = password_hash.hash(user.password)

    created_user = create_user(
        email=user.email,
        hashed_password=hashed_password,
        repository=repository,
    )

    return RegisterResponse(
        id=created_user.id,
        email=created_user.email,
        message="User registered successfully",
    )


def login_user(
    credentials: LoginRequest,
    repository: UserRepository,
) -> TokenResponse:
    user = repository.get_by_email(credentials.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not password_hash.verify(
        credentials.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )