from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
