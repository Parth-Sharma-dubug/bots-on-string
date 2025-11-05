from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatBase(BaseModel):
    question: str
    answer: Optional[str] = None

class ChatCreate(ChatBase):
    visitor_id: int
    chatbot_id: int

class ChatOut(ChatBase):
    id: int
    visitor_id: int
    chatbot_id: int
    created_at: datetime

    class Config:
        orm_mode = True
