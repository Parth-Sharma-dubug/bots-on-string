# app/api/api_v1/routes/chatbot.py
from typing import List, Generator, Optional

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.chatbot import ChatbotCreate, ChatbotRead, ChatbotUpdate, ChatbotOut
from app.models.chatbot import Chatbot
from app.models.company import Company
from app.auth.deps import get_current_company_id


# service functions that integrate LangChain + Qdrant; implemented in app.services.chatbot_service
from app.services.chatbot_service import (
    train_chatbot_from_files,
    train_chatbot_from_url,
    query_chatbot,  
)

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


def get_db() -> Generator[Session, None, None]:
    """
    Simple DB dependency using your SessionLocal factory.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#
# CRUD for Chatbots
#
@router.post("/create")
def create_chatbot(payload: ChatbotCreate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == payload.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    bot = Chatbot(
        name=payload.name,
        description=payload.description,
        company_id=payload.company_id,
    )
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot


@router.get("/", response_model=List[ChatbotOut])
def list_chatbots(db: Session = Depends(get_db)):
    return db.query(Chatbot).all()


# get chatbots for a company:
@router.get("/chatbots", response_model=List[ChatbotOut])
def list_company_chatbots(
    db: Session = Depends(get_db),
    current_company_id: int = Depends(get_current_company_id),
):
    chatbots = db.query(Chatbot).filter(
        Chatbot.company_id == current_company_id
    ).all()
    return chatbots


@router.get("/company/{company_id}", response_model=List[ChatbotOut])
def list_company_chatbots(company_id: int, db: Session = Depends(get_db)):
    return db.query(Chatbot).filter(Chatbot.company_id == company_id).all()


@router.get("/{chatbot_id}", response_model=ChatbotOut)
def read_chatbot(chatbot_id: int, db: Session = Depends(get_db)):
    bot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chatbot not found")
    return bot


@router.put("/{chatbot_id}", response_model=ChatbotOut)
def update_chatbot(chatbot_id: int, data: ChatbotUpdate, db: Session = Depends(get_db)):
    bot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chatbot not found")

    if data.name is not None:
        bot.name = data.name
    if data.description is not None:
        bot.description = data.description

    db.commit()
    db.refresh(bot)
    return bot


@router.delete("/{chatbot_id}", status_code=status.HTTP_200_OK)
def delete_chatbot(chatbot_id: int, db: Session = Depends(get_db)):
    bot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chatbot not found")
    db.delete(bot)
    db.commit()
    return {"message": "Chatbot deleted successfully"}

#
# Query endpoint — this is the endpoint your frontend expects:
# POST /chatbot/{chatbot_id}/query  with JSON body: { "company_id": 1, "query": "hello" }
#
@router.post("/{chatbot_id}/query")
async def query_chatbot_route(
    chatbot_id: int,
    company_id: int = Form(...),
    query: str = Form(...)
):
    """
    Query chatbot by ID (with company_id + query passed in form).
    """
    response = await query_chatbot(company_id, chatbot_id, query)
    if not response:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    return response

