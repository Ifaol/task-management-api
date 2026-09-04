from app.modules.tasks.repository import TaskRepository
from app.modules.users.repository import UserRepository


task_repository = TaskRepository()
user_repository = UserRepository()


def get_task_repository() -> TaskRepository:
    return task_repository


def get_user_repository() -> UserRepository:
    return user_repository