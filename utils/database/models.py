from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from typing import Any

class APIBaseModel(DeclarativeBase):
    id: Any
    __name__

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__
