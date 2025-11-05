from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CompanyOut(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
