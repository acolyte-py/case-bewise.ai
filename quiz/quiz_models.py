from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class Question(Base):
    """Модель для вопросов из викторины"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question_text = Column(String)
    answer_question = Column(String)
    create_data = Column(DateTime)


class QuizRequest(BaseModel):
    """Модель для POST запроса /quiz"""
    questions_num: int
