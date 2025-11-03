from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class VisitorSession(Base):
    __tablename__ = "visitor_sessions"

    id = Column(Integer, primary_key=True, index=True)
    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"), nullable=False)  # ✅ ADD THIS LINE

    started_at = Column(DateTime)
    ended_at = Column(DateTime)

    visitor = relationship("Visitor", back_populates="sessions")
    chatbot = relationship("Chatbot", back_populates="visitor_sessions")  # ✅ ensure this matches Chatbot model
