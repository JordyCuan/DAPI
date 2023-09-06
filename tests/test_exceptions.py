import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException, status

from utils.exceptions.client import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    TimeoutException,
    UnauthorizedException,
)
from utils.exceptions.generic import HTTPBaseException
from utils.exceptions.server import DatabaseConnectionError, ServerError


class TestHttpBaseExceptionSuperCall(unittest.TestCase):
    def test_http_base_exception_super_is_called(self) -> None:
        with patch.object(HTTPException, "__init__", MagicMock()) as mock_super_init:
            HTTPBaseException.status_code = 500
            HTTPBaseException.detail = "Test"
            _ = HTTPBaseException()
            mock_super_init.assert_called_once()


class TestClientExceptions:
    def test_bad_request_exception(self):
        exception = BadRequestException()
        assert exception.status_code == status.HTTP_400_BAD_REQUEST
        assert exception.detail.startswith("Bad Request")

    def test_unauthorized_exception(self):
        exception = UnauthorizedException()
        assert exception.status_code == status.HTTP_401_UNAUTHORIZED
        assert exception.detail.startswith("Not authorized")

    def test_forbidden_exception(self):
        exception = ForbiddenException()
        assert exception.status_code == status.HTTP_403_FORBIDDEN
        assert exception.detail.startswith("Forbidden")

    def test_not_found_exception(self):
        exception = NotFoundException()
        assert exception.status_code == status.HTTP_404_NOT_FOUND
        assert exception.detail.startswith("Not Found")

    def test_timeout_exception(self):
        exception = TimeoutException()
        assert exception.status_code == status.HTTP_408_REQUEST_TIMEOUT
        assert exception.detail.startswith("Process timed out")


class TestServerExceptions:
    def test_bad_request_exception(self):
        exception = ServerError()
        assert exception.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exception.detail.startswith("Internal Server Error")

    def test_unauthorized_exception(self):
        exception = DatabaseConnectionError()
        assert exception.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exception.detail.startswith("Could not connect or perform the operation to the database")
