from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.modules.workspaces.model import Workspace
from app.modules.workspaces.repository import WorkspaceRepository
from app.modules.workspaces.schema import (
    WorkspaceCreate,
    WorkspaceResponse,
)


def create_workspace(
    workspace: WorkspaceCreate,
    repository: WorkspaceRepository,
) -> WorkspaceResponse:
    now = datetime.now(timezone.utc)

    new_workspace = Workspace(
        id=uuid4(),
        name=workspace.name,
        created_at=now,
    )

    created_workspace = repository.create(new_workspace)

    return WorkspaceResponse.model_validate(created_workspace)


def get_workspaces(
    repository: WorkspaceRepository,
) -> list[WorkspaceResponse]:
    workspaces = repository.get_all()

    return [
        WorkspaceResponse.model_validate(workspace)
        for workspace in workspaces
    ]


def get_workspace(
    workspace_id: UUID,
    repository: WorkspaceRepository,
) -> WorkspaceResponse:
    workspace = repository.get_by_id(workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    return WorkspaceResponse.model_validate(workspace)


def update_workspace(
    workspace_id: UUID,
    workspace_update: WorkspaceCreate,
    repository: WorkspaceRepository,
) -> WorkspaceResponse:
    workspace = repository.get_by_id(workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    workspace.name = workspace_update.name

    updated_workspace = repository.update(workspace)

    return WorkspaceResponse.model_validate(updated_workspace)


def delete_workspace(
    workspace_id: UUID,
    repository: WorkspaceRepository,
) -> None:
    workspace = repository.get_by_id(workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    repository.delete(workspace_id)