from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session, DeclarativeBase

load_dotenv()


class Base(DeclarativeBase):
    pass


url = URL.create(
    "postgresql",
    username=getenv("POSTGRES_USERNAME"),
    password=getenv("POSTGRES_PASSWORD"),
    host=getenv("POSTGRES_HOST"),
    port=getenv("POSTGRES_PORT"),
    database=getenv("POSTGRES_DBNAME"),
)
engine = create_engine(url, echo=True)


def get_session() -> Session:
    return Session(engine)
