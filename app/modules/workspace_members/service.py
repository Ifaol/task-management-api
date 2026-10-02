from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status

from app.modules.workspace_members.model import WorkspaceMember
from app.modules.workspace_members.repository import WorkspaceMemberRepository
from app.modules.workspace_members.schema import (
    WorkspaceMemberCreate,
    WorkspaceMemberResponse,
)
from app.modules.users.repository import UserRepository
from app.modules.workspaces.repository import WorkspaceRepository


def create_workspace_member(
    workspace_id: UUID,
    member: WorkspaceMemberCreate,
    repository: WorkspaceMemberRepository,
    workspace_repository: WorkspaceRepository,
    user_repository: UserRepository,
) -> WorkspaceMemberResponse:
    workspace = workspace_repository.get_by_id(workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    user = user_repository.get_by_id(member.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    existing_member = repository.get_by_id(
        workspace_id,
        member.user_id,
    )

    if existing_member is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a member of this workspace",
        )

    new_member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=member.user_id,
        role=member.role,
        joined_at=datetime.now(timezone.utc),
    )

    created_member = repository.create(new_member)

    return WorkspaceMemberResponse.model_validate(created_member)


def get_workspace_members(
    workspace_id: UUID,
    repository: WorkspaceMemberRepository,
    workspace_repository: WorkspaceRepository,
) -> list[WorkspaceMemberResponse]:
    workspace = workspace_repository.get_by_id(workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    members = repository.get_by_workspace(workspace_id)

    return [
        WorkspaceMemberResponse.model_validate(member)
        for member in members
    ]


def get_workspace_member(
    workspace_id: UUID,
    user_id: UUID,
    repository: WorkspaceMemberRepository,
) -> WorkspaceMemberResponse:
    member = repository.get_by_id(
        workspace_id,
        user_id,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace member not found",
        )

    return WorkspaceMemberResponse.model_validate(member)


def update_workspace_member(
    workspace_id: UUID,
    user_id: UUID,
    member_update: WorkspaceMemberCreate,
    repository: WorkspaceMemberRepository,
) -> WorkspaceMemberResponse:
    member = repository.get_by_id(
        workspace_id,
        user_id,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace member not found",
        )

    member.role = member_update.role

    updated_member = repository.update(member)

    return WorkspaceMemberResponse.model_validate(updated_member)


def delete_workspace_member(
    workspace_id: UUID,
    user_id: UUID,
    repository: WorkspaceMemberRepository,
) -> None:
    member = repository.get_by_id(
        workspace_id,
        user_id,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace member not found",
        )

    repository.delete(
        workspace_id,
        user_id,
    )