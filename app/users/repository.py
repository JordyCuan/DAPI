from typing import Optional

from utils.crypt import get_bcrypt_context
from utils.database.repository import BaseRepository

from .models import User

bcrypt_context = get_bcrypt_context(schemes=["bcrypt"], deprecated="auto")


class UserRepository(BaseRepository[User]):
    model = User

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.retrieve(username=username, hashed_password=password)

        if not user:
            return None
        if not bcrypt_context.verify_password(password, user.hashed_password):
            return None
        return user
