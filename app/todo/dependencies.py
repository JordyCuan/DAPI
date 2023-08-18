from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.core import get_database

from .filters import TodoFilterManager, TodoFilterSchema
from .repository import TodoRepository
from .services import TodoService


def get_todo_repository(session: Session = Depends(get_database)) -> TodoRepository:
    return TodoRepository(session=session)


def get_todo_service(repository: TodoRepository = Depends(get_todo_repository)) -> TodoService:
    return TodoService(repository=repository)


def get_todo_filter_manager(filters: TodoFilterSchema = Depends()) -> TodoFilterManager:
    return TodoFilterManager(filters=filters)