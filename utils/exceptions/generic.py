"""
This module provides generic exceptions for applications.
It allows for more specific error handling and detailed error responses.
"""
from typing import Any, Dict, Optional

from fastapi import HTTPException


class HTTPBaseException(HTTPException):
    """
    Base class for custom HTTP exceptions in FastAPI applications.
    """

    status_code: int
    detail: str

    def __init__(self, *, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None) -> None:
        detail = f"{self.detail} - {detail}" if detail else self.detail
        super().__init__(
            status_code=self.status_code,
            detail=detail,
            headers=headers,
        )


class ImproperlyConfigured(Exception):
    """Class is somehow improperly configured"""

    pass
