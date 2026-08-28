from uuid import UUID
from .schema import TaskResponse


class TaskRepository:
    def __init__(self):
        self.tasks: dict[UUID, TaskResponse] = {}

    def create(self, task: TaskResponse) -> TaskResponse:
        self.tasks[task.id] = task

        return task

    def get_all(self) -> list[TaskResponse]:
        return list(self.tasks.values())

    def get_by_id(self, task_id: UUID) -> TaskResponse | None:
        return self.tasks.get(task_id)

    def update(self, task: TaskResponse) -> TaskResponse:
        self.tasks[task.id] = task

        return task

    def delete(self, task_id: UUID) -> None:
        del self.tasks[task_id]


task_repository = TaskRepository()