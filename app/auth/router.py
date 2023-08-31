from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from app.settings import settings
from app.users.models import User
from utils.crypt import get_bcrypt_context
from utils.exceptions.client import BadRequestException

from .dependencies import valid_user_credentials
from .schemas import Token
from .security import create_access_token

bcrypt_context = get_bcrypt_context(schemes=["bcrypt"], deprecated="auto")


oauth_bearer = OAuth2PasswordBearer(tokenUrl="token/")


router = APIRouter(prefix="/token", tags=["auth"])


@router.post("/", response_model=Token)
async def login_access_token(user: User = Depends(valid_user_credentials)) -> Any:
    if user.is_active:
        raise BadRequestException(detail="Inactive user")

    token = create_access_token(
        user.username,
        user.id,
        secret_key=settings.SECRET_KEY,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    # We need this structure. More: https://stackoverflow.com/questions/59808854/swagger-authorization-bearer-not-send
    return {"access_token": token, "token_type": "bearer"}
