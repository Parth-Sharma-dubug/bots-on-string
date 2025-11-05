from fastapi import APIRouter
from . import company, chatbot, chat, visitor

router = APIRouter()

router.include_router(company.router, prefix="/companies", tags=["Companies"])
router.include_router(chatbot.router, prefix="/chatbots", tags=["Chatbots"])
router.include_router(visitor.router, prefix="/visitors", tags=["Visitors"])
router.include_router(chat.router, prefix="/chat", tags=["Chat"])
