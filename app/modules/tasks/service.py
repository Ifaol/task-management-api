from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.modules.tasks.model import Task
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.schema import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)


def create_task(
    task: TaskCreate,
    repository: TaskRepository,
) -> TaskResponse:
    now = datetime.now(timezone.utc)

    new_task = Task(
        id=uuid4(),
        workspace_id=task.workspace_id,
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date,
        assigned_user_id=task.assigned_user_id,
        created_at=now,
        updated_at=now,
    )

    created_task = repository.create(new_task)

    return TaskResponse.model_validate(created_task)


def get_tasks(
    repository: TaskRepository,
) -> list[TaskResponse]:
    tasks = repository.get_all()

    return [
        TaskResponse.model_validate(task)
        for task in tasks
    ]


def get_task(
    task_id: UUID,
    repository: TaskRepository,
) -> TaskResponse:
    task = repository.get_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.model_validate(task)


def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    repository: TaskRepository,
) -> TaskResponse:
    task = repository.get_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    update_data = task_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.now(timezone.utc)

    updated_task = repository.update(task)

    return TaskResponse.model_validate(updated_task)


def delete_task(
    task_id: UUID,
    repository: TaskRepository,
) -> None:
    task = repository.get_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    repository.delete(task_id)