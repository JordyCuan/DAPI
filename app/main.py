from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.database import APIBaseModel, engine
from app.settings import settings
from app.todo.router import router as todo_router
from utils.middleware import SQLAlchemyExceptionHandlerMiddleware

app = FastAPI(debug=settings.DEBUG)

APIBaseModel.metadata.create_all(bind=engine)

app.add_middleware(SQLAlchemyExceptionHandlerMiddleware, debug=settings.DEBUG)

app.include_router(auth_router)
app.include_router(todo_router)
