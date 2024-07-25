from sqlalchemy.orm import Mapped, mapped_column
from config.db import Base
from sqlalchemy import ForeignKey


class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[int] = mapped_column()
    enabled: Mapped[bool] = mapped_column()
    server_id: Mapped[int] = mapped_column(ForeignKey("server.id"))