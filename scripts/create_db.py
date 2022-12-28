from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine.connect())

    session.execute("""create table user (
        id integer not null primary key,
        email varchar(256),
        password varchar(256),
        login varchar(256)
    );""")

    session.execute("""create table auth_token (
            id integer not null primary key,
            token varchar(256),
            user_id integer references user,
            created_at varchar(64)
        );""")

    session.execute("""create table stream (
            id integer not null primary key,
            user_id integer references user,
            title VARCHAR,
            topic VARCHAR,
            status VARCHAR(64),
            created_at VARCHAR(64)
        );""")

    session.close()


if __name__ == '__main__':
    main()
