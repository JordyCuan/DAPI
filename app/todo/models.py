from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.users.models import User  # noqa: F401


class Todo(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title = Mapped[str]
    description = Mapped[str]
    priority = Mapped[int]
    complete: Mapped[bool] = mapped_column(default=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="todos")
