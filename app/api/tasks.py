from uuid import UUID

from fastapi import APIRouter, status

from ..modules.tasks.schema import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from ..modules.tasks.service import (
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
def create_task_route(task: TaskCreate) -> TaskResponse:
    return create_task(task)


@router.get(
    "/",
    response_model=list[TaskResponse],
)
def get_tasks_route() -> list[TaskResponse]:
    return get_tasks()


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task_route(task_id: UUID) -> TaskResponse:
    return get_task(task_id)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task_route(
    task_id: UUID,
    task_update: TaskUpdate,
) -> TaskResponse:
    return update_task(task_id, task_update)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_route(task_id: UUID) -> None:
    delete_task(task_id)