from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


# Base user schema (shared)
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = "user"  # could be 'admin', 'manager', 'user'


# For creating a new user
class UserCreate(UserBase):
    password: str
    company_id: Optional[UUID]  # link user to a company


# For returning user info (e.g., API response)
class UserResponse(UserBase):
    id: UUID
    company_id: Optional[UUID]

    class Config:
        orm_mode = True
