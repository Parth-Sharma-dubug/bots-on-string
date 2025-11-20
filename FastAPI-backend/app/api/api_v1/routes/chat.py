from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.models.chat import Chat
from app.models.visitor import Visitor
# from app.schemas.chat import ChatCreate, ChatOut
from app.core.database import get_db
from datetime import datetime, timedelta
# from typing import List
from pydantic import BaseModel
from app.services.qdrant_service import search_similar_vectors
# from app.services.openai_service import generate_reply
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.visitor import Visitor
from app.models.visitor_session import VisitorSession
from app.models.chatbot import Chatbot

router = APIRouter(prefix="/chat", tags=["chat"])

class MessageIn(BaseModel):
    visitor_anonymous_id: str | None = None
    session_id: int | None = None
    message: str
    context: list[dict] | None = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from app.services.ollama_service import generate_reply

@router.post("/{chatbot_id}/message")
async def send_message(chatbot_id: int, payload: MessageIn, db: Session = Depends(get_db)):
    # Locate chatbot
    chatbot = db.get(Chatbot, chatbot_id)
    if not chatbot:
        raise HTTPException(404, "Chatbot not found")

    else:
        visitor = Visitor(anonymous_id=payload.visitor_anonymous_id or "anon-" + str(uuid.uuid4()))
        db.add(visitor)
        db.commit()
        db.refresh(visitor)
        session = VisitorSession(visitor_id=visitor.id, chatbot_id=chatbot_id)
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save visitor message
    chat = Chat(visitor_session_id=session.id, chatbot_id=chatbot_id, role="visitor", message=payload.message)
    db.add(chat)
    db.commit()
    db.refresh(chat)

    # 🧠 Generate bot reply via Ollama + Qdrant
    try:
        bot_text = await generate_reply(payload.message, chatbot_id)
    except Exception as e:
        bot_text = f"⚠️ Local AI error: {str(e)}"

    # Save bot reply
    bot_chat = Chat(visitor_session_id=session.id, chatbot_id=chatbot_id, role="bot", message=bot_text)
    db.add(bot_chat)
    db.commit()

    return {"reply": bot_text, "session_id": session.id}



@router.post("/{chatbot_id}/ollamaTesting")
async def send_message(chatbot_id: str, payload: MessageIn):
    

    print("received payload:", payload)
    print("chatbot_id:", chatbot_id)

    # 🧠 Generate bot reply via Ollama + Qdrant
    try:
        bot_text = await generate_reply(payload.message, chatbot_id, history = payload.context)
    except Exception as e:
        import traceback
        traceback.print_exc()   # <-- add this
        bot_text = f"⚠️ Local AI error: {str(e)}"


    return {"reply": bot_text}





