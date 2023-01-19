import os
from starlette.config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL моей бд
dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3]

config = Config(f'{root_dir}.env')

# строка подключения
SQLALCHAMY_DATABASE_URL = 'sqlite:///./investcalc_app.db'

# создаем движок SqlAlchemy
engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={
    "check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# создаем базовый класс для моделей
Base = declarative_base()


# устанавливаем подключение к бд
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
