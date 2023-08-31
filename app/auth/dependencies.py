from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_database
from app.users.models import User
from app.users.repository import UserRepository
from utils.exceptions.client import NotFoundException


def valid_user_credentials(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_database)
) -> User:
    repository = UserRepository(session=session)
    user = repository.authenticate(form_data.username, form_data.password)

    if not user:
        raise NotFoundException(detail="Invalid user credential")

    return user
