from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    due_date: datetime | None = None
    assigned_user_id: UUID | None = None


class TaskCreate(TaskBase):
    workspace_id: UUID


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    status: TaskStatus | None = None
    due_date: datetime | None = None
    assigned_user_id: UUID | None = None


class TaskResponse(TaskBase):
    id: UUID
    workspace_id: UUID
    created_at: datetime
    updated_at: datetime