from sqlalchemy.orm import Mapped, mapped_column
from config.db import Base


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
