"""Fastapi dependencies to interact with database."""
from typing import Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from utils.database.repository import BaseRepository

from .core import get_database

_T = TypeVar("_T", bound=BaseRepository)


def apply_session(target: Type[_T]) -> Callable[[Session], _T]:
    def _apply_session(session: Session = Depends(get_database)) -> _T:
        return target(session=session)

    return _apply_session


from pydantic import BaseModel


def apply_serialization(target: Type[_T]) -> Callable[[Session], _T]:
    def _apply_serialization(serialized: Session = Depends(get_database)) -> _T:
        return target(payload=serialized)

    return _apply_serialization
