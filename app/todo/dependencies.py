from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.core import get_database
from utils.pagination import LimitOffsetPagination, LimitOffsetSchema

from .filters import FilterParam, TodoFilterManager, TodoFilterSchema
from .repository import TodoRepository
from .services import TodoService


def get_todo_repository(session: Session = Depends(get_database)) -> TodoRepository:
    return TodoRepository(session=session)


def get_todo_service(repository: TodoRepository = Depends(get_todo_repository)) -> TodoService:
    return TodoService(repository=repository)


def get_todo_filter_manager(
    filters: TodoFilterSchema = Depends(),
    # ordering: Annotated[list[str] | None, Query()] = None,
    ordering: Optional[list[str]] = FilterParam(),
) -> TodoFilterManager:
    return TodoFilterManager(filters=filters, ordering=ordering)


# TODO: This one might be "global" for project due its (possible) immutable across domains nature
def get_pagination(pagination: LimitOffsetSchema = Depends()) -> LimitOffsetPagination:
    return LimitOffsetPagination(pagination)
