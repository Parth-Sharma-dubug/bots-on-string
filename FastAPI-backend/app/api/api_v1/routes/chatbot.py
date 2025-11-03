from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.chatbot import Chatbot
from app.models.company import Company
from app.schemas.chatbot import ChatbotCreate, ChatbotOut, ChatbotUpdate
from app.core.database import get_db
from typing import List

router = APIRouter(prefix="/chatbots", tags=["Chatbots"])

@router.post("/", response_model=ChatbotOut)
def create_chatbot(bot: ChatbotCreate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == bot.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    chatbot = Chatbot(
        name=bot.name,
        description=bot.description,
        company_id=bot.company_id,
    )
    db.add(chatbot)
    db.commit()
    db.refresh(chatbot)
    return chatbot

@router.get("/", response_model=List[ChatbotOut])
def get_all_chatbots(db: Session = Depends(get_db)):
    return db.query(Chatbot).all()

@router.get("/company/{company_id}", response_model=List[ChatbotOut])
def get_company_chatbots(company_id: int, db: Session = Depends(get_db)):
    return db.query(Chatbot).filter(Chatbot.company_id == company_id).all()

@router.get("/{chatbot_id}", response_model=ChatbotOut)
def get_chatbot(chatbot_id: int, db: Session = Depends(get_db)):
    bot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    return bot

@router.put("/{chatbot_id}", response_model=ChatbotOut)
def update_chatbot(chatbot_id: int, data: ChatbotUpdate, db: Session = Depends(get_db)):
    bot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    if data.name:
        bot.name = data.name
    if data.description:
        bot.description = data.description
    db.commit()
    db.refresh(bot)
    return bot

@router.delete("/{chatbot_id}")
def delete_chatbot(chatbot_id: int, db: Session = Depends(get_db)):
    bot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    db.delete(bot)
    db.commit()
    return {"message": "Chatbot deleted successfully"}
