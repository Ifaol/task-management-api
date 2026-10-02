import jwt

from collections.abc import Generator
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.modules.tasks.repository import TaskRepository
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.workspaces.repository import WorkspaceRepository
from app.modules.workspace_members.repository import WorkspaceMemberRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_task_repository(
    db: Session = Depends(get_db),
) -> TaskRepository:
    return TaskRepository(db)


def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


def get_workspace_repository(
    db: Session = Depends(get_db),
) -> WorkspaceRepository:
    return WorkspaceRepository(db)


def get_workspace_member_repository(
    db: Session = Depends(get_db),
) -> WorkspaceMemberRepository:
    return WorkspaceMemberRepository(db)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = UUID(payload["sub"])
    except (
        KeyError,
        ValueError,
        jwt.InvalidTokenError,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user