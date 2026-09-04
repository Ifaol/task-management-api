from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserInDB(BaseModel):
    id: UUID
    email: EmailStr
    hashed_password: str
    is_active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime