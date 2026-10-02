from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.dependencies import (
    get_user_repository,
    get_workspace_member_repository,
    get_workspace_repository,
)
from app.core.rbac import RequireRole
from app.modules.users.repository import UserRepository
from app.modules.workspace_members.repository import WorkspaceMemberRepository
from app.modules.workspace_members.schema import (
    WorkspaceMemberCreate,
    WorkspaceMemberResponse,
    WorkspaceMemberRole,
)
from app.modules.workspace_members.service import (
    create_workspace_member,
    delete_workspace_member,
    get_workspace_member,
    get_workspace_members,
    update_workspace_member,
)
from app.modules.workspaces.repository import WorkspaceRepository


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace Members"],
)


@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workspace_member_route(
    workspace_id: UUID,
    member: WorkspaceMemberCreate,
    current_user=Depends(
        RequireRole(WorkspaceMemberRole.OWNER),
    ),
    repository: WorkspaceMemberRepository = Depends(
        get_workspace_member_repository,
    ),
    workspace_repository: WorkspaceRepository = Depends(
        get_workspace_repository,
    ),
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
) -> WorkspaceMemberResponse:
    return create_workspace_member(
        workspace_id,
        member,
        repository,
        workspace_repository,
        user_repository,
    )


@router.get(
    "/{workspace_id}/members",
    response_model=list[WorkspaceMemberResponse],
)
def get_workspace_members_route(
    workspace_id: UUID,
    current_user=Depends(
        RequireRole(WorkspaceMemberRole.VIEWER),
    ),
    repository: WorkspaceMemberRepository = Depends(
        get_workspace_member_repository,
    ),
    workspace_repository: WorkspaceRepository = Depends(
        get_workspace_repository,
    ),
) -> list[WorkspaceMemberResponse]:
    return get_workspace_members(
        workspace_id,
        repository,
        workspace_repository,
    )


@router.get(
    "/{workspace_id}/members/{user_id}",
    response_model=WorkspaceMemberResponse,
)
def get_workspace_member_route(
    workspace_id: UUID,
    user_id: UUID,
    current_user=Depends(
        RequireRole(WorkspaceMemberRole.VIEWER),
    ),
    repository: WorkspaceMemberRepository = Depends(
        get_workspace_member_repository,
    ),
) -> WorkspaceMemberResponse:
    return get_workspace_member(
        workspace_id,
        user_id,
        repository,
    )


@router.patch(
    "/{workspace_id}/members/{user_id}",
    response_model=WorkspaceMemberResponse,
)
def update_workspace_member_route(
    workspace_id: UUID,
    user_id: UUID,
    member_update: WorkspaceMemberCreate,
    current_user=Depends(
        RequireRole(WorkspaceMemberRole.OWNER),
    ),
    repository: WorkspaceMemberRepository = Depends(
        get_workspace_member_repository,
    ),
) -> WorkspaceMemberResponse:
    return update_workspace_member(
        workspace_id,
        user_id,
        member_update,
        repository,
    )


@router.delete(
    "/{workspace_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_workspace_member_route(
    workspace_id: UUID,
    user_id: UUID,
    current_user=Depends(
        RequireRole(WorkspaceMemberRole.OWNER),
    ),
    repository: WorkspaceMemberRepository = Depends(
        get_workspace_member_repository,
    ),
) -> None:
    delete_workspace_member(
        workspace_id,
        user_id,
        repository,
    )