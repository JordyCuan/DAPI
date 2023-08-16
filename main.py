from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.todo.router import router as todo_router

# from app.database import engine
# from utils.database.models import APIBaseModel
from utils.middleware import SQLAlchemyExceptionHandlerMiddleware

app = FastAPI()

# APIBaseModel.metadata.create_all(bind=engine)

app.add_middleware(SQLAlchemyExceptionHandlerMiddleware)

app.include_router(auth_router)
app.include_router(todo_router)

# TODO: Move to ./app directory


# app.exception_handlers.setdefault(SQLAlchemyError, sqlalchemy_exception_handler)


# async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
#     return JSONResponse(
#         status_code=HTTP_422_UNPROCESSABLE_ENTITY,
#         content={"detail": jsonable_encoder(exc.errors())},
#     )


# app.exception_handlers.setdefault(SQLAlchemyError, sqlalchemy_exception_handler)
