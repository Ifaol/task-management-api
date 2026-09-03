from app.modules.tasks.repository import TaskRepository

task_repository = TaskRepository()


def get_task_repository() -> TaskRepository:
    return task_repository