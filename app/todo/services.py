from utils.services import BaseService

from .repository import TodoRepository


class TodoService(BaseService):
    # Explicitly set `__init__()` method for better compatibility with typing and mypy
    def __init__(self, *, repository: TodoRepository):
        super().__init__(repository=repository)
