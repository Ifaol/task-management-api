from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import HTTPException, status

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
    task_id = uuid4()
    now = datetime.now(timezone.utc)

    new_task = TaskResponse(
        id=task_id,
        workspace_id=task.workspace_id,
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date,
        assigned_user_id=task.assigned_user_id,
        created_at=now,
        updated_at=now,
    )

    return repository.create(new_task)


def get_tasks(
    repository: TaskRepository,
) -> list[TaskResponse]:
    return repository.get_all()


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

    return task


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

    updated_task = task.model_copy(
        update={
            **update_data,
            "updated_at": datetime.now(timezone.utc),
        }
    )

    return repository.update(updated_task)


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