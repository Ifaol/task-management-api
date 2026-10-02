from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.workspace_members.model import WorkspaceMember


class WorkspaceMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, member: WorkspaceMember) -> WorkspaceMember:
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def get_by_id(
        self,
        workspace_id: UUID,
        user_id: UUID,
    ) -> WorkspaceMember | None:
        statement = select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )

        return self.db.scalars(statement).first()

    def get_by_workspace(
        self,
        workspace_id: UUID,
    ) -> list[WorkspaceMember]:
        statement = select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
        )

        return list(self.db.scalars(statement).all())

    def get_by_user(
        self,
        user_id: UUID,
    ) -> list[WorkspaceMember]:
        statement = select(WorkspaceMember).where(
            WorkspaceMember.user_id == user_id,
        )

        return list(self.db.scalars(statement).all())

    def update(self, member: WorkspaceMember) -> WorkspaceMember:
        self.db.commit()
        self.db.refresh(member)
        return member

    def delete(
        self,
        workspace_id: UUID,
        user_id: UUID,
    ) -> None:
        member = self.get_by_id(
            workspace_id,
            user_id,
        )

        if member is not None:
            self.db.delete(member)
            self.db.commit()