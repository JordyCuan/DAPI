from datetime import datetime
from typing import TypeVar

from sqlalchemy import Connection, event
from sqlalchemy.orm import Mapped, Mapper, mapped_column

T = TypeVar("T", bound="TimestampMixin")


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    @staticmethod
    def _timestamp_before_update(mapper: Mapper[T], connection: Connection, target: T) -> None:
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls) -> None:
        event.listen(cls, "before_update", cls._timestamp_before_update)
