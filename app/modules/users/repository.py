from uuid import UUID

from app.modules.users.schema import UserInDB


class UserRepository:
    def __init__(self):
        self.users: dict[UUID, UserInDB] = {}

    def create(self, user: UserInDB) -> UserInDB:
        self.users[user.id] = user

        return user

    def get_all(self) -> list[UserInDB]:
        return list(self.users.values())

    def get_by_id(self, user_id: UUID) -> UserInDB | None:
        return self.users.get(user_id)

    def get_by_email(self, email: str) -> UserInDB | None:
        for user in self.users.values():
            if user.email == email:
                return user

        return None

    def update(self, user: UserInDB) -> UserInDB:
        self.users[user.id] = user

        return user

    def delete(self, user_id: UUID) -> None:
        del self.users[user_id]