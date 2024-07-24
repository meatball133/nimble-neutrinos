from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.engine.url import URL
from os import getenv


class Base(DeclarativeBase):
    pass


url = URL.create(
    "postgresql",
    username=getenv("POSTGRES_USERNAME"),
    password=getenv("POSTGRES_PASSWORD"),
    host=getenv("POSTGRES_HOST"),
    database=getenv("POSTGRES_DBNAME"),
)
engine = create_engine(url, echo=True)


def get_session() -> Session:
    return Session(engine)
