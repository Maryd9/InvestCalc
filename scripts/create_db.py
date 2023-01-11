import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app import settings
from app.config import SQLALCHAMY_DATABASE_URL
from app.main import app


def main():
    engine = create_engine(SQLALCHAMY_DATABASE_URL)
    session = Session(bind=engine.connect())

    session.execute("""create table user (
        id integer not null primary key,
        email varchar(256),
        password varchar(256),
        username varchar(256),
        created_at varchar(64)
    );""")

    session.execute("""create table auth_token (
            id integer not null primary key,
            token varchar(256),
            user_id integer references user,
            created_at varchar(64)
        );""")


    session.close()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.settings.server_host, port=settings.settings.server_port, reload=True)
