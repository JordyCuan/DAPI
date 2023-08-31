"""
This module provides exceptions for server errors (5XX).
"""
from fastapi import status

from .generic import HTTPBaseException


class ServerError(HTTPBaseException):
    """
    The server has encountered a situation it does not know how to handle.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal Server Error"


class DatabaseConnectionError(ServerError):
    """
    The server has encountered an issue performing the database operation.
    """

    detail = "Could not connect or perform the operation to the database"
