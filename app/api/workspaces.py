from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.dependencies import (
    get_current_user,
    get_workspace_member_repository,
    get_workspace_repository,
)
from app.core.rbac import RequireRole
from app.modules.users.model import User
from app.modules.workspace_members.repository import WorkspaceMemberRepository
from app.modules.workspace_members.schema import WorkspaceMemberRole
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
    current_user: User = Depends(get_current_user),
    repository: WorkspaceRepository = Depends(
        get_workspace_repository,
    ),
    member_repository: WorkspaceMemberRepository = Depends(
        get_workspace_member_repository,
    ),
) -> WorkspaceResponse:
    return create_workspace(
        workspace=workspace,
        repository=repository,
        member_repository=member_repository,
        user_id=current_user.id,
    )


@router.get(
    "/",
    response_model=list[WorkspaceResponse],
)
def get_workspaces_route(
    current_user: User = Depends(get_current_user),
    repository: WorkspaceRepository = Depends(
        get_workspace_repository,
    ),
) -> list[WorkspaceResponse]:
    return get_workspaces(repository)


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def get_workspace_route(
    workspace_id: UUID,
    current_user: User = Depends(
        RequireRole(WorkspaceMemberRole.VIEWER),
    ),
    repository: WorkspaceRepository = Depends(
        get_workspace_repository,
    ),
) -> WorkspaceResponse:
    return get_workspace(
        workspace_id,
        repository,
    )


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def update_workspace_route(
    workspace_id: UUID,
    workspace_update: WorkspaceCreate,
    current_user: User = Depends(
        RequireRole(WorkspaceMemberRole.OWNER),
    ),
    repository: WorkspaceRepository = Depends(
        get_workspace_repository,
    ),
) -> WorkspaceResponse:
    return update_workspace(
        workspace_id,
        workspace_update,
        repository,
    )


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_workspace_route(
    workspace_id: UUID,
    current_user: User = Depends(
        RequireRole(WorkspaceMemberRole.OWNER),
    ),
    repository: WorkspaceRepository = Depends(
        get_workspace_repository,
    ),
) -> None:
    delete_workspace(
        workspace_id,
        repository,
    )