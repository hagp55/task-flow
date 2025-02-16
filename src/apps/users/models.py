from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None]
    password: Mapped[str | None]
    email: Mapped[str | None]
    google_access_token: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
