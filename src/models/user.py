from sqlalchemy.orm import Mapped, mapped_column
from src.config.db import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[int] = mapped_column()
    access_token: Mapped[str] = mapped_column()
    refresh_token: Mapped[str] = mapped_column()
