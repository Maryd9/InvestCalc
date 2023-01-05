from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from sqlalchemy import create_engine


def choose_db(arg_db):
    engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False}, echo=True)
    return engine


def get_db():
    db_session_local = SessionLocal()
    try:
        yield db_session_local
    finally:
        db_session_local.close()


check_db = choose_db(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=check_db)
