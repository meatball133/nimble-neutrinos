from config.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, ForeignKey, Column
from models.tags import Tag
from typing import List

association_table = Table(
    "tags_content",
    Base.metadata,
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
    Column("content_id", ForeignKey("content.id"), primary_key=True),
)


class Content(Base):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    tags: Mapped[List[Tag]] = relationship(secondary=association_table)
