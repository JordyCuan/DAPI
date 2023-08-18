from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.router import get_current_user
from app.database.core import get_database
from utils.exceptions import NotFoundException, UnauthorizedException

from .dependencies import get_todo_filter_manager, get_todo_service
from .filters import TodoFilterManager, TodoFilterSchema
from .models import Todo as TodoModel
from .repository import Todo as TodoModel
from .schemas import Todo as TodoSchema
from .services import TodoService

# from utils.schemas.filters import FilterParams, OrderParams, PaginationParams


router = APIRouter(prefix="/todo", tags=["todo"])

# una dependencia sencilla llamada "validate_authenticated_user"
# Un Mixin para traer al usuario


@router.get("/")
async def list_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_database)):
    if user is None:
        raise UnauthorizedException
    return db.query(TodoModel).filter(TodoModel.owner_id == user.get("id")).all()


@router.get("/{todo_id}")
async def get_todo_by_user(
    todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException

    todo_model = (
        db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == todo_id).first()
    )
    if todo_model is None:
        raise NotFoundException

    return todo_model


@router.post("/", status_code=201)
async def create_todo_by_user(
    todo: TodoSchema, user: dict = Depends(get_current_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException

    todo_model = TodoModel(**todo.model_dump())
    todo_model.owner_id = user.get("id")
    db.add(todo_model)
    db.commit()
    return todo_model


@router.put("/{id}")
async def update_todo_by_user(
    id: int,
    todo: TodoSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    if user is None:
        raise UnauthorizedException

    todo_model = db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == id).first()
    if not todo_model:
        raise NotFoundException

    todo_data = todo.model_dump(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo_model, key, value)

    db.add(todo_model)
    db.commit()
    return todo_model


@router.delete("/{id}", status_code=204)
async def destroy_todo_by_user(
    id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException

    todo_model = db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == id).first()
    if not todo_model:
        raise NotFoundException

    db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == id).delete()
    db.commit()
    return {}


###################################################
# BORRAR


router = APIRouter(prefix="/todo", tags=["todo"])


TodoServiceAnnotation = Annotated[TodoService, Depends(get_todo_service)]


@router.get("/{id}", status_code=200)
async def read_item(id: int, service: TodoServiceAnnotation):
    return service.get_by_id(id=id)


@router.get("/", status_code=200)
async def get_all_todo(
    service: TodoServiceAnnotation,
    filter_manager: TodoFilterManager = Depends(get_todo_filter_manager),
):
    return service.list(filter_manager=filter_manager)


@router.post("/", status_code=201)
async def create_todo(payload: TodoSchema, service: TodoServiceAnnotation):
    data = payload.model_dump()
    service.create(entity=data)
    return data


@router.put("/{id}")
async def update_todo(id: int, payload: TodoSchema, service: TodoServiceAnnotation):
    data = payload.model_dump(exclude_unset=True)
    service.update(id=id, entity=data)
    return data


@router.delete("/{id}", status_code=204)
async def destroy_todo(id: int, service: TodoServiceAnnotation):
    return service.destroy(id=id)
