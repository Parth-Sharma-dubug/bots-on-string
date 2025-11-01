from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatResponse
from app.services.openai_service import generate_gpt_response
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post("/", response_model=ChatResponse)
async def chat_with_bot(chat_input: ChatCreate, db: Session = Depends(get_db)):
    try:
        response_text = await generate_gpt_response(chat_input.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error from GPT: {str(e)}")

    chat = Chat(
        user_id=chat_input.user_id,
        company_id=chat_input.company_id,
        message=chat_input.message,
        response=response_text,
        created_at=datetime.utcnow(),
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat
