from typing import Any, Callable, Coroutine, Dict, Type, Union

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import NoResultFound, SQLAlchemyError, TimeoutError
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.testclient import TestClient

from utils.middleware import SQLAlchemyExceptionHandlerMiddleware


def raise_no_result_found() -> None:
    raise NoResultFound()


def raise_timeout_error() -> None:
    raise TimeoutError()


def raise_general_sqlalchemy_error() -> None:
    raise SQLAlchemyError()  # A generic exception not mapped


def route_with_http_exception() -> None:
    raise HTTPException(status_code=400)


def route_with_request_validation_exception(param: int) -> None:
    pass  # pragma: no cover


def route_with_server_error() -> None:
    raise RuntimeError("Oops!")


def no_error() -> Dict[str, str]:
    return {"message": "No error here"}


def raise_no_content_error() -> None:
    raise HTTPException(status_code=204)


async def http_exception_handler(request: Request, exception: HTTPException) -> JSONResponse:
    return JSONResponse({"exception": "http-exception"})


async def request_validation_exception_handler(
    request: Request, exception: RequestValidationError
) -> JSONResponse:
    return JSONResponse({"exception": "request-validation"})


async def server_error_exception_handler(request: Request, exception: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"exception": "server-error"})


exception_handlers: Dict[
    Union[int, Type[Exception]], Callable[[Request, Any], Coroutine[Any, Any, Response]]
] = {
    HTTPException: http_exception_handler,
    RequestValidationError: request_validation_exception_handler,
    Exception: server_error_exception_handler,
}


class TestSQLAlchemyExceptionHandlerMiddleware:
    @pytest.fixture(autouse=True)
    def setup_class(self) -> None:
        # Dummy API to integrate the middleware and simulate exceptions
        self.test_app = FastAPI()
        self.test_app.add_middleware(SQLAlchemyExceptionHandlerMiddleware, debug=True)

        # Manually decorated
        self.test_app.get("/raise-no-result-found")(raise_no_result_found)
        self.test_app.get("/raise-timeout-error")(raise_timeout_error)
        self.test_app.get("/raise-general-sqlalchemy-error")(raise_general_sqlalchemy_error)
        self.test_app.get("/no-error")(no_error)
        self.test_app.get("/raise-no-content-error")(raise_no_content_error)

        self.client = TestClient(self.test_app)

    def test_no_result_found(self) -> None:
        response = self.client.get("/raise-no-result-found")
        assert response.status_code == 404
        assert response.json()["detail"] == "Not Found"

    def test_timeout_error(self) -> None:
        response = self.client.get("/raise-timeout-error")
        assert response.status_code == 408
        assert response.json()["detail"] == "Process timed out"

    def test_general_sqlalchemy_error(self) -> None:
        response = self.client.get("/raise-general-sqlalchemy-error")
        assert response.status_code == 500
        assert response.json()["detail"] == "Could not connect or perform the operation to the database"

    def test_no_exceptions(self) -> None:
        response = self.client.get("/no-error")
        assert response.status_code == 200
        assert response.json() == {"message": "No error here"}

    def test_no_content_error(self) -> None:
        response = self.client.get("/raise-no-content-error")
        assert response.status_code == 204
        assert response.text == ""

    def test_override_http_exception(self) -> None:
        app = FastAPI(exception_handlers=exception_handlers)
        app.get("/http-exception")(route_with_http_exception)
        client = TestClient(app)
        response = client.get("/http-exception")
        assert response.status_code == 200
        assert response.json() == {"exception": "http-exception"}

    def test_override_request_validation_exception(self) -> None:
        app = FastAPI(exception_handlers=exception_handlers)
        app.get("/request-validation/{param}/")(route_with_request_validation_exception)
        client = TestClient(app)
        response = client.get("/request-validation/invalid")
        assert response.status_code == 200
        assert response.json() == {"exception": "request-validation"}

    def test_override_server_error_exception_raises(self) -> None:
        app = FastAPI(exception_handlers=exception_handlers)
        app.get("/server-error")(route_with_server_error)
        client = TestClient(app)
        with pytest.raises(RuntimeError):
            client.get("/server-error")

    def test_override_server_error_exception_response(self) -> None:
        app = FastAPI(exception_handlers=exception_handlers)
        app.get("/server-error")(route_with_server_error)
        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/server-error")
        assert response.status_code == 500
        assert response.json() == {"exception": "server-error"}
