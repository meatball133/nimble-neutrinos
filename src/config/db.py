from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.engine.url import URL

class Base(DeclarativeBase):
    pass

url = URL.create(
    "postgresql",
    username="postgres",
    password="postgres",
    host="localhost",
    database="nimble"
)
engine = create_engine(url, echo=True)


def get_session() -> Session:
    return Session(engine)
