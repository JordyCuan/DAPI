"""Fastapi dependencies to interact with database."""
from typing import Callable, Generator, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from utils.database.repository import BaseRepository

from .core import session_maker

T = TypeVar("T", bound=BaseRepository)


def get_database() -> Generator[Session, None, None]:
    try:
        db = session_maker()
        yield db
    finally:
        db.close()


def apply_session(target: Type[T]) -> Callable[[Session], T]:
    def _apply_session(session: Session = Depends(get_database)) -> T:
        return target(session=session)

    return _apply_session
