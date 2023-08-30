from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_database
from utils.crypt import get_bcrypt_context

from .models import User
from .schemas import CreateUser

bcrypt_context = get_bcrypt_context(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create/user", status_code=201)
async def create_new_user(schema: CreateUser, db: Session = Depends(get_database)) -> Any:
    data = schema.model_dump(exclude_unset=True, exclude_none=True)
    password = data.pop("password")
    user_model = User(hashed_password=bcrypt_context.get_password_hash(password), **data)

    db.add(user_model)
    db.commit()
    return {}
