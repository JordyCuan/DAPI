from starlette.responses import JSONResponse as JSONResponse  # noqa

"""
This module provides custom responses for applications.
It allows for more specific error handling and detailed error responses.
"""

from typing import Any, Optional


class BaseErrorResponse(JSONResponse):
    """
    Base class for custom HTTP responses in FastAPI/Starlette applications.
    """

    status_code: int
    detail: str

    def __init__(
        self,
        debug_message: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            content=self.get_content(debug_message),
            status_code=self.status_code,
            **kwargs,
        )

    def get_content(self, debug_message: Optional[str]) -> Any:
        content = {"detail": self.detail}
        if debug_message:
            content["debug_message"] = debug_message
        return content


class NotFoundErrorResponse(BaseErrorResponse):
    """
    The server cannot find the requested resource.
    """

    status_code = 404
    detail = "Not Found"


class TimeoutErrorResponse(BaseErrorResponse):
    """
    This response is sent on an idle connection by the server.
    """

    status_code = 408
    detail = "Process timed out"


class DatabaseErrorResponse(BaseErrorResponse):
    """
    The server has encountered an issue performing the database operation.
    """

    status_code = 500
    detail = "Could not connect or perform the operation to the database"
