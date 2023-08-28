"""Fastapi dependencies to interact with database."""
from typing import Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from utils.database.repository import BaseRepository

from .core import get_database

T = TypeVar("T", bound=BaseRepository)


def apply_session(target: Type[T]) -> Callable[[Session], T]:
    def _apply_session(session: Session = Depends(get_database)) -> T:
        return target(session=session)

    return _apply_session
