from utils.services import BaseService

from .repository import TodoRepository


class TodoService(BaseService[TodoRepository]):
    pass
