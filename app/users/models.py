from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import APIBaseModel

if TYPE_CHECKING:
    from app.todo.models import Todo  # noqa: F401


class User(APIBaseModel):
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    firstname: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    is_active: Mapped[bool] = mapped_column(default=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)

    todos: Mapped[list["Todo"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
