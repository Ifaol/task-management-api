from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.workspaces.model import Workspace


class WorkspaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, workspace: Workspace) -> Workspace:
        self.db.add(workspace)
        self.db.commit()
        self.db.refresh(workspace)
        return workspace

    def get_all(self) -> list[Workspace]:
        statement = select(Workspace)
        return list(self.db.scalars(statement).all())

    def get_by_id(self, workspace_id: UUID) -> Workspace | None:
        return self.db.get(Workspace, workspace_id)

    def update(self, workspace: Workspace) -> Workspace:
        self.db.commit()
        self.db.refresh(workspace)
        return workspace

    def delete(self, workspace_id: UUID) -> None:
        workspace = self.get_by_id(workspace_id)

        if workspace is not None:
            self.db.delete(workspace)
            self.db.commit()