from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from ..modules.tasks.schema import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


# In-memory task storage
tasks: dict[UUID, TaskResponse] = {}


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate):
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


@router.get(
    "/",
    response_model=list[TaskResponse],
)
def get_tasks():
    return list(tasks.values())


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(task_id: UUID):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(task_id: UUID, task_update: TaskUpdate):
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


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: UUID):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    del tasks[task_id]