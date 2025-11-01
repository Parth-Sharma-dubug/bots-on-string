from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class ChatBase(BaseModel):
    user_id: UUID
    company_id: UUID
    message: str


class ChatCreate(ChatBase):
    pass


class ChatResponse(BaseModel):
    id: UUID
    user_id: UUID
    company_id: UUID
    message: str
    response: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
