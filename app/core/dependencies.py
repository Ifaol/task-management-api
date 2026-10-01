from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.modules.tasks.repository import TaskRepository
from app.modules.users.repository import UserRepository


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