from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database.core import get_database
from app.settings import settings
from app.users.models import User
from utils.auth import get_bcrypt_context
from utils.exceptions import NotFoundException

bcrypt_context = get_bcrypt_context(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

oauth_bearer = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(prefix="", tags=["auth"])


def authenticate_user(username: str, password: str, db):
    user: User = db.query(User).filter(User.username == username).first()

    if not user:
        return None
    if not bcrypt_context.verify_password(password, user.password):
        return None
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    now = datetime.utcnow()

    expire = now + timedelta(minutes=15)
    if expires_delta:
        expire = now + expires_delta

    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise NotFoundException  # TODO - Unauthorized?
        return {"username": username, "id": user_id}
    except JWTError as exc:
        raise NotFoundException from exc


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_database)
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise NotFoundException

    token = create_access_token(user.username, user.id)
    # We need this structure. More: https://stackoverflow.com/questions/59808854/swagger-authorization-bearer-not-send
    return {"access_token": token, "token_type": "bearer"}
