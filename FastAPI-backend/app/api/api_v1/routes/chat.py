from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.models.visitor import Visitor
from app.schemas.chat import ChatCreate, ChatOut
from app.core.database import get_db
from datetime import datetime, timedelta
from typing import List

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatOut)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    visitor = db.query(Visitor).filter(Visitor.id == chat.visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")

    if datetime.utcnow() - visitor.created_at.replace(tzinfo=None) > timedelta(hours=1):
        raise HTTPException(status_code=410, detail="Session expired")

    db_chat = Chat(
        visitor_id=chat.visitor_id,
        chatbot_id=chat.chatbot_id,
        question=chat.question,
        answer="(GPT response will go here)",
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@router.get("/visitor/{visitor_id}", response_model=List[ChatOut])
def get_visitor_chats(visitor_id: int, db: Session = Depends(get_db)):
    return db.query(Chat).filter(Chat.visitor_id == visitor_id).order_by(Chat.created_at).all()
