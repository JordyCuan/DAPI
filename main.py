from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.todo.router import router as todo_router

# from app.database import engine
# from utils.database.models import APIBaseModel

app = FastAPI()

# APIBaseModel.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(todo_router)

# TODO: Move to ./app directory


from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


# @app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc._message())},
    )


app.exception_handlers.setdefault(SQLAlchemyError, sqlalchemy_exception_handler)


# async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
#     return JSONResponse(
#         status_code=HTTP_422_UNPROCESSABLE_ENTITY,
#         content={"detail": jsonable_encoder(exc.errors())},
#     )


# app.exception_handlers.setdefault(SQLAlchemyError, sqlalchemy_exception_handler)
