from typing import Optional, Type

from fastapi import Request, Response
from fastapi.utils import is_body_allowed_for_status_code
from sqlalchemy.exc import NoResultFound, SQLAlchemyError, TimeoutError
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.types import ASGIApp

from .responses import BaseErrorResponse, DatabaseErrorResponse, NotFoundErrorResponse, TimeoutErrorResponse


# NOTE: HTTPExceptions are automatically handled by the `ExceptionMiddleware` class
# from the `starlette.middleware.exceptions` module, which FastAPI extends/inherits.
# In this context, we're only handling other types of exceptions (e.g., SQLAlchemy ones),
# allowing developers to focus directly on business rules.
#
# With love,
# Jordy Cuan
class SQLAlchemyExceptionHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        dispatch: Optional[DispatchFunction] = None,
        debug: bool = False,
    ) -> None:
        self.app = app
        self.dispatch_func = self.dispatch if dispatch is None else dispatch
        self.debug = debug
        self._exception_responses: dict[Type[Exception], Type[BaseErrorResponse]] = {
            NoResultFound: NotFoundErrorResponse,
            TimeoutError: TimeoutErrorResponse,
        }

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
            return response
        except SQLAlchemyError as exc:
            error_response = self._exception_responses.get(type(exc), DatabaseErrorResponse)
            status_code = error_response.status_code
            debug_message = str(exc) if self.debug else None

            # NOTE: This is not necessary since fastapi exception handlers handle this part before it
            # reaches in here. This is going to be remove on future commit and left as is right now
            # just for references.
            if not is_body_allowed_for_status_code(status_code):
                return Response(status_code=status_code)
            return error_response(debug_message=debug_message)
