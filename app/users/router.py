from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.core import get_database
from utils.auth import get_bcrypt_context

from .models import User
from .schemas import CreateUser

bcrypt_context = get_bcrypt_context(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create/user", status_code=201)
async def create_new_user(user: CreateUser, db: Session = Depends(get_database)):
    user_model = User(**user.dict())
    user_model.password = bcrypt_context.get_password_hash(user_model.password)

    db.add(user_model)
    db.commit()
    return {}
