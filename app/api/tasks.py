from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_task_repository
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.schema import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.modules.tasks.service import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    update_task,
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_route(
    task: TaskCreate,
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskResponse:
    return create_task(task, repository)


@router.get(
    "/",
    response_model=list[TaskResponse],
)
def get_tasks_route(
    repository: TaskRepository = Depends(get_task_repository),
) -> list[TaskResponse]:
    return get_tasks(repository)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task_route(
    task_id: UUID,
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskResponse:
    return get_task(task_id, repository)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task_route(
    task_id: UUID,
    task_update: TaskUpdate,
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskResponse:
    return update_task(task_id, task_update, repository)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_route(
    task_id: UUID,
    repository: TaskRepository = Depends(get_task_repository),
) -> None:
    delete_task(task_id, repository)