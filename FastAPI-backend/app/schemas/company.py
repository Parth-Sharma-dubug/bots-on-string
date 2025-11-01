from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from app.schemas.user import UserResponse


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    owner_id: Optional[UUID]


class CompanyResponse(CompanyBase):
    id: UUID
    users: Optional[List[UserResponse]] = []  # all users under company

    class Config:
        orm_mode = True
