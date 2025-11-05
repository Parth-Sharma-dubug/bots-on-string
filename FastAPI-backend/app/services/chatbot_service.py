# app/services/chatbot_service.py
from sqlalchemy.orm import Session
from app.models.chatbot import Chatbot

def create_chatbot(db: Session, name: str, description: str, company_id: int):
    bot = Chatbot(name=name, description=description, company_id=company_id)
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot

def list_chatbots(db: Session, company_id: int):
    return db.query(Chatbot).filter(Chatbot.company_id == company_id).all()

def get_chatbot(db: Session, bot_id: int):
    return db.query(Chatbot).filter(Chatbot.id == bot_id).first()

def update_chatbot(db: Session, bot: Chatbot, **fields):
    for k, v in fields.items():
        setattr(bot, k, v)
    db.commit()
    db.refresh(bot)
    return bot

def delete_chatbot(db: Session, bot: Chatbot):
    db.delete(bot)
    db.commit()
