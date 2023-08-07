from utils.database.repository import BaseRepository

from .models import Todo


class TodoRepository(BaseRepository):
    model = Todo
