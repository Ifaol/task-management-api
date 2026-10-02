from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_workspace_repository
from app.modules.workspaces.repository import WorkspaceRepository
from app.modules.workspaces.schema import (
    WorkspaceCreate,
    WorkspaceResponse,
)
from app.modules.workspaces.service import (
    create_workspace,
    delete_workspace,
    get_workspace,
    get_workspaces,
    update_workspace,
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.post(
    "/",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workspace_route(
    workspace: WorkspaceCreate,
    repository: WorkspaceRepository = Depends(get_workspace_repository),
) -> WorkspaceResponse:
    return create_workspace(workspace, repository)


@router.get(
    "/",
    response_model=list[WorkspaceResponse],
)
def get_workspaces_route(
    repository: WorkspaceRepository = Depends(get_workspace_repository),
) -> list[WorkspaceResponse]:
    return get_workspaces(repository)


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def get_workspace_route(
    workspace_id: UUID,
    repository: WorkspaceRepository = Depends(get_workspace_repository),
) -> WorkspaceResponse:
    return get_workspace(workspace_id, repository)


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def update_workspace_route(
    workspace_id: UUID,
    workspace: WorkspaceCreate,
    repository: WorkspaceRepository = Depends(get_workspace_repository),
) -> WorkspaceResponse:
    return update_workspace(
        workspace_id,
        workspace,
        repository,
    )


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_workspace_route(
    workspace_id: UUID,
    repository: WorkspaceRepository = Depends(get_workspace_repository),
) -> None:
    delete_workspace(workspace_id, repository)