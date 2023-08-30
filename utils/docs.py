from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class FastAPIRouteParameters(BaseModel):
    """
    Defines route parameters involved in the OpenAPI documentation for a FastAPI.
    """

    tags: Optional[List[str]] = None
    """
    A list of strings that will be used to group endpoints together in
    the documentation interface. As an example, `tags=["items"]` will cause the
    endpoint to be grouped under the "items" category in the documentation.
    """

    summary: Optional[str] = None
    """
    A short, concise summary of what the endpoint does. It will be
    prominently displayed in the OpenAPI documentation.
    """

    description: Optional[str] = None
    """
    Provides a more detailed description of the endpoint. This
    information is typically displayed when you expand the endpoint details in
    the documentation.
    """

    response_description: Optional[str] = "Successful Response"
    """
    Allows you to provide a custom description for the response. This description is
    shown next to the response status code in the OpenAPI docs.
    """

    status_code: int = 200
    """
    You can set a custom default status code for the response using this parameter. This
    status code will be shown as the default response in the documentation.
    """

    deprecated: bool = False
    """If set to `True`, it will mark the endpoint as deprecated in the documentation."""

    include_in_schema: bool = True
    """Determines if the endpoint should appear in the OpenAPI documentation."""

    operation_id: Optional[str] = None
    """
    An identifier for the operation. Used for client generation or other tools. If not
    provided, FastAPI will generate one based on the path and the method.

    Note:
    -----
    This is for advanced usage
    """

    responses: Dict[Union[int, str], Dict[str, Any]] = {}
    """
    Allows you to declare additional response classes, other than the default one, along with their status codes and models. This parameter helps document possible responses your API can send beyond the default one.

    Note:
    -----
    This is for advanced usage

    Example:
    --------

    ```python
    from fastapi import HTTPException

    @app.get("/endpoint/", responses={404: {"model": HTTPException, "description": "Item not found"}})
    ```
    """

    name: Optional[str] = None
    """
    Primarily used for OpenAPI documentation and the dependency injection system.

    Note:
    -----
    This is for advanced usage

    Warning:
    --------
    * If you're using the name parameter for the OpenAPI operationId, ensure that it's unique across your entire API.
    * If you're using it for dependency overrides, ensure that the names you provide make sense and don't unintentionally clash with other parts of your code.
    """

    openapi_extra: Optional[Dict[str, Any]] = None
    """
    Allows for additional customization or extension of the OpenAPI schema for the specific route. Useful for adding or modifying
    details that FastAPI might not handle natively or for fine-tuning the schema according to specific requirements.

    See more: https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#openapi-extra

    Note:
    -----
    This is for advanced usage
    """
