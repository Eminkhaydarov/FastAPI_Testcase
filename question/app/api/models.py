from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class QuestionModel(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime(timezone=True))
    add_at = Column(DateTime, default=datetime.utcnow)
