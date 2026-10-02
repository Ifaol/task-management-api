from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WorkspaceMemberRole(StrEnum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


class WorkspaceMemberCreate(BaseModel):
    user_id: UUID
    role: WorkspaceMemberRole = WorkspaceMemberRole.VIEWER


class WorkspaceMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workspace_id: UUID
    user_id: UUID
    role: WorkspaceMemberRole
    joined_at: datetime