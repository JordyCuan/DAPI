from utils.database.repository import BaseRepository

from .models import User


class TodoRepository(BaseRepository):
    model = User
