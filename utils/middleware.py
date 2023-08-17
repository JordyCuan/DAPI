from sqlalchemy.exc import NoResultFound, SQLAlchemyError, TimeoutError
from starlette.middleware.base import BaseHTTPMiddleware

from .exceptions import NotFoundException, ServerError, TimeoutException


class SQLAlchemyExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
        except NoResultFound as exc:
            raise NotFoundException from exc
        except TimeoutError as exc:
            raise TimeoutException from exc
        # TODO: Is it necessary to handle MultipleObjectsReturned?
        # except SQLAlchemyError as exc:
        #     raise ServerError  # Global default server exception for any other SQLAlchemy error
        return response
