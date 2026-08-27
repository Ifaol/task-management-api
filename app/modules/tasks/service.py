from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from .schema import TaskCreate, TaskResponse, TaskUpdate


# In-memory task storage
tasks: dict[UUID, TaskResponse] = {}


def create_task(task: TaskCreate) -> TaskResponse:
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

    tasks[task_id] = new_task

    return new_task


def get_tasks() -> list[TaskResponse]:
    return list(tasks.values())


def get_task(task_id: UUID) -> TaskResponse:
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
) -> TaskResponse:
    task = tasks.get(task_id)

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

    tasks[task_id] = updated_task

    return updated_task


def delete_task(task_id: UUID) -> None:
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    del tasks[task_id]