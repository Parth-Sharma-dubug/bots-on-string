from pydantic import BaseModel
from datetime import datetime
from typing import List

class VisitorBase(BaseModel):
    session_id: str

class VisitorCreate(BaseModel):
    chatbot_id: int

class VisitorOut(VisitorBase):
    id: int
    chatbot_id: int
    created_at: datetime

    class Config:
        orm_mode = True
