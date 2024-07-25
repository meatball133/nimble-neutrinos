from config.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, ForeignKey, Column
from models.tags import Tag
from typing import List

association_table = Table(
    "tags_messages",
    Base.metadata,
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
    Column("message_id", ForeignKey("message.id"), primary_key=True),
)


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    discord_id: Mapped[int] = mapped_column()
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"))
    tags: Mapped[List[Tag]] = relationship(secondary=association_table)
