from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Chatbot(Base):
    __tablename__ = "chatbots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))

    # ✅ Use string reference to avoid circular import issues
    company = relationship("Company", back_populates="chatbots")

    visitor_sessions = relationship("VisitorSession", back_populates="chatbot")
