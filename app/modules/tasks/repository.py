from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.tasks.model import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

    def get_all(self) -> list[Task]:
        statement = select(Task)

        return list(self.db.scalars(statement).all())

    def get_by_id(self, task_id: UUID) -> Task | None:
        return self.db.get(Task, task_id)

    def update(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)

        return task

    def delete(self, task_id: UUID) -> None:
        task = self.get_by_id(task_id)

        if task is not None:
            self.db.delete(task)
            self.db.commit()