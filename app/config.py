import os

from starlette.config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .settings import settings

VERSION = '0.0.1'

# URL моей бд
dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3]

config = Config(f'{root_dir}.env')

DEBUG = config('DEBUG', cast=bool, default=False)

PROJECT_NAME = config('PROJECT_NAME', default='InvestCalc App Api')

SQLALCHAMY_DATABASE_URL = 'sqlite:///./investcalc_app.db'

engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={
    "check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, )

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
