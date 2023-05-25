from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from datetime import datetime
from uuid import uuid4, UUID


Base = declarative_base()


class Users(Base):
    """Модель для пользователей сервиса"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    token = Column(String(36), default=lambda: str(uuid4()))


class Audio(Base):
    """Модель для музыки пользователей сервиса"""
    __tablename__ = "audio"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", backref="audio")
    filename = Column(String(100))
    create_at = Column(DateTime, default=datetime.now())
    url = Column(String(100), default=lambda: str(uuid4()))


class UsersRequests(BaseModel):
    """Модель для POST запроса /users"""
    name: str


class AudioRequests(BaseModel):
    """Модель для POST запроса /audio/{user_id}"""
    url: str
    user_id: int
    audio_id: UUID
