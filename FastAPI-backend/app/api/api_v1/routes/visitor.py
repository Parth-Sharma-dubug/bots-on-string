from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.visitor import Visitor
from app.models.chatbot import Chatbot
from app.schemas.visitor import VisitorCreate, VisitorOut
from app.core.database import get_db
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/visitors", tags=["Visitors"])

@router.post("/", response_model=VisitorOut)
def create_visitor(visitor: VisitorCreate, db: Session = Depends(get_db)):
    chatbot = db.query(Chatbot).filter(Chatbot.id == visitor.chatbot_id).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")

    session_id = str(uuid.uuid4())
    new_visitor = Visitor(session_id=session_id, chatbot_id=visitor.chatbot_id)
    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)
    return new_visitor

@router.get("/{session_id}", response_model=VisitorOut)
def get_visitor(session_id: str, db: Session = Depends(get_db)):
    visitor = db.query(Visitor).filter(Visitor.session_id == session_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")

    # expire after 1 hour
    if datetime.utcnow() - visitor.created_at.replace(tzinfo=None) > timedelta(hours=1):
        db.delete(visitor)
        db.commit()
        raise HTTPException(status_code=410, detail="Session expired")

    return visitor
