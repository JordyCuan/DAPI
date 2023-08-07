"""
This module provides custom exceptions for applications.
It allows for more specific error handling and detailed error responses.
"""

from typing import Any, Dict, Optional

from fastapi import HTTPException


class HTTPBaseException(HTTPException):
    """
    Base class for custom HTTP exceptions in FastAPI applications.
    """

    def __init__(self, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, headers=headers)


class BadRequestException(HTTPBaseException):
    """
    The server cannot or will not process the request due to something that is perceived to be a client error
    """

    status_code = 400
    detail = "Bad Request"


class UnauthorizedException(HTTPBaseException):
    """
    The client must authenticate itself to get the requested response.
    """

    status_code = 401
    detail = "Not authorized for this operation"


class ForbiddenException(HTTPBaseException):
    """
    The client does not have access rights to the content, Unlike 401 Unauthorized, the client's identity is known to the server.
    """

    status_code = 403
    detail = "Not authorized for this operation"


class NotFoundException(HTTPBaseException):
    """
    The server cannot find the requested resource.
    """

    status_code = 404
    detail = "Not Found"


class TimeoutException(HTTPBaseException):
    """
    This response is sent on an idle connection by the server.
    """

    status_code = 408
    detail = "Process timed out"


class ServerError(HTTPBaseException):
    """
    The server has encountered a situation it does not know how to handle.
    """

    status_code = 500
    detail = "Internal Server Error"


class DatabaseConnectionError(ServerError):
    """
    The server has encountered an issue performing the database operation.
    """

    detail = "Could not connect or perform the operation to the database"


class ImproperlyConfigured(Exception):
    """Class is somehow improperly configured"""

    pass
