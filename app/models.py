from enum import Enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from app.config import DATABASE_URL

Base = declarative_base()


def connect_db():
    engine = create_engine(DATABASE_URL, connect_args={})
    session = Session(bind=engine.connect())
    return session


class StreamStatus(Enum):
    PLANED = 'planed'
    ACTIVE = 'active'
    CLOSED = 'closed'


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    login = Column(String)

    def __str__(self):
        return f'[{self.id}]{self.email}'

    def get_filtered_data(self):
        return {
            'email': self.email,
            'login': self.login
        }


class AuthToken(Base):
    __tablename__ = 'auth_token'
    id = Column(Integer, primary_key=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(String, default=datetime.utcnow())


class Stream(Base):
    __tablename__ = 'stream'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String)
    topic = Column(String)
    status = Column(String, default=StreamStatus.PLANED.value)
    created_at = Column(String, default=datetime.utcnow())

    def __str__(self):
        return f'{self.id} - {self.title}[{self.topic}]'
