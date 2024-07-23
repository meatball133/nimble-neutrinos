from sqlalchemy.orm import Mapped, mapped_column
from config.db import Base


class Server(Base):
    __tablename__ = "server"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[int] = mapped_column()