"""
This module provides exceptions for client errors (4XX).
"""

from fastapi import status

from .generic import HTTPBaseException


class BadRequestException(HTTPBaseException):
    """
    The server cannot or will not process the request due to something that is perceived to be a client error
    """

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad Request"


class UnauthorizedException(HTTPBaseException):
    """
    The client must authenticate itself to get the requested response.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Not authorized for this operation"


class ForbiddenException(HTTPBaseException):
    """
    The client does not have access rights to the content, Unlike 401 Unauthorized, the client's identity is known to the server.
    """

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Forbidden resource access"


class NotFoundException(HTTPBaseException):
    """
    The server cannot find the requested resource.
    """

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not Found"


class TimeoutException(HTTPBaseException):
    """
    This response is sent on an idle connection by the server.
    """

    status_code = status.HTTP_408_REQUEST_TIMEOUT
    detail = "Process timed out"
