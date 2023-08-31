from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.security import get_authenticated_user
from app.database import get_database
from utils.exceptions.client import NotFoundException, UnauthorizedException
from utils.pagination import LimitOffsetPagination

from .dependencies import get_pagination, get_todo_filter_manager, get_todo_service
from .docs import create_todo_docs, destroy_todo_docs, list_todo_docs, retrieve_todo_docs, update_todo_docs
from .filters import TodoFilterManager, TodoFilterSchema
from .models import Todo as TodoModel
from .schemas import TodoSchema
from .services import TodoService

router_auth = APIRouter(prefix="/todo/auth", tags=["todo"])


@router_auth.get("/")
async def list_todo_by_user(
    user: dict = Depends(get_authenticated_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException
    return db.query(TodoModel).filter(TodoModel.owner_id == user.get("id")).all()


@router_auth.get("/{todo_id}")
async def retrieve_todo_by_user(
    todo_id: int, user: dict = Depends(get_authenticated_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException

    todo_model = (
        db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == todo_id).first()
    )
    if todo_model is None:
        raise NotFoundException

    return todo_model


@router_auth.post("/", status_code=201)
async def create_todo_by_user(
    todo: TodoSchema, user: dict = Depends(get_authenticated_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException

    todo_model = TodoModel(**todo.model_dump())
    todo_model.owner_id = user.get("id")
    db.add(todo_model)
    db.commit()
    return todo_model


@router_auth.put("/{id}")
async def update_todo_by_user(
    id: int,
    todo: TodoSchema,
    user: dict = Depends(get_authenticated_user),
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


@router_auth.delete("/{id}", status_code=204)
async def destroy_todo_by_user(
    id: int, user: dict = Depends(get_authenticated_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException

    todo_model = db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == id).first()
    if not todo_model:
        raise NotFoundException

    db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == id).delete()
    db.commit()
    return {}


##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

router = APIRouter(prefix="/todo", tags=["todo"])


TodoServiceAnnotation = Annotated[TodoService, Depends(get_todo_service)]


@router.get("/{id}", **retrieve_todo_docs)
async def retrieve_todo(id: int, service: TodoServiceAnnotation):
    return service.get_by_id(id=id)


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
