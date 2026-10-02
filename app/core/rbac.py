from uuid import UUID

from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.modules.users.model import User
from app.modules.workspace_members.repository import WorkspaceMemberRepository
from app.modules.workspace_members.schema import WorkspaceMemberRole
from app.core.dependencies import get_workspace_member_repository


class RequireRole:
    def __init__(self, required_role: WorkspaceMemberRole):
        self.required_role = required_role

    def __call__(
        self,
        workspace_id: UUID,
        current_user: User = Depends(get_current_user),
        repository: WorkspaceMemberRepository = Depends(
            get_workspace_member_repository,
        ),
    ) -> User:
        member = repository.get_by_id(
            workspace_id,
            current_user.id,
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this workspace",
            )

        role_permissions = {
            WorkspaceMemberRole.OWNER: 3,
            WorkspaceMemberRole.EDITOR: 2,
            WorkspaceMemberRole.VIEWER: 1,
        }

        if role_permissions[member.role] < role_permissions[self.required_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient workspace permissions",
            )

        return current_user