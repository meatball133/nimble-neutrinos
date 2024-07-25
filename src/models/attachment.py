from sqlalchemy.orm import Mapped, mapped_column
from src.config.db import Base, engine


class Attachment(Base):
    __tablename__ = "attachment"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[int] = mapped_column()
    message_id: Mapped[int] = mapped_column()
