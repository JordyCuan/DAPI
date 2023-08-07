from sqlalchemy import MappingResult

"""Fastapi dependencies to interact with database."""
from typing import Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from utils.database.repository import BaseRepository

# from .core import get_database

_T = TypeVar("_T", bound=BaseRepository)


# def apply_session(target: Type[_T]) -> Callable[[Session], _T]:
#     def _apply_session(session: Session = Depends(get_database)) -> _T:
#         return target(session=session)

#     return _apply_session


# async def valid_model_id(id: int) -> MappingResult:
#     post = await service.get_by_id(id=id)
#     if not post:
#         raise PostNotFound()

#     return post
