from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.router import get_current_user
from app.database.core import get_database
from utils.exceptions import NotFoundException, UnauthorizedException

from .dependencies import get_pagination, get_todo_filter_manager, get_todo_service
from .docs import create_todo_docs, destroy_todo_docs, list_todo_docs, retrieve_todo_docs, update_todo_docs
from .filters import TodoFilterManager, TodoFilterSchema
from .models import Todo as TodoModel
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

# NOTE: IMPORTANT! Wherever we refer to basic http methods operations (ie. get, post, update, delete) we use retrieve, list, create, update, destroy


@router.get("/{id}", **retrieve_todo_docs)
async def retrieve_todo(id: int, service: TodoServiceAnnotation):
    return service.get_by_id(id=id)


from utils.pagination import LimitOffsetPagination


@router.get("/", **list_todo_docs)
async def list_todo(
    service: TodoServiceAnnotation,
    filter_manager: TodoFilterManager = Depends(get_todo_filter_manager),
    pagination_manager: LimitOffsetPagination = Depends(get_pagination),
):
    return service.list(filter_manager=filter_manager, pagination_manager=pagination_manager)


@router.post("/", **create_todo_docs)
async def create_todo(payload: TodoSchema, service: TodoServiceAnnotation):
    data = payload.model_dump()
    service.create(entity=data)
    return data


@router.put("/{id}", **update_todo_docs)
async def update_todo(id: int, payload: TodoSchema, service: TodoServiceAnnotation):
    data = payload.model_dump(exclude_unset=True)
    return service.update(id=id, entity=data)


@router.delete("/{id}", **destroy_todo_docs)
async def destroy_todo(id: int, service: TodoServiceAnnotation):
    return service.destroy(id=id)
