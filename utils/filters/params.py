"""
params.py

This module provides custom parameter classes tailored for API processing.

The module currently includes the following classes:

- `FilterParam`: A custom query parameter class tailored for filtering purposes.

Usage:
------
These classes can be imported and used as dependencies in FastAPI route functions
to extract and process different parameters or other parts of the HTTP request.

Example:
--------
```
from .params import FilterParam

@app.get("/items/")
def get_items(filter: Optional[str] = FilterParam(...)):
    ...
```

Note:
-----
When extending or adding new classes, ensure they align with FastAPI's request parsing mechanisms.
"""
from typing import Any

from fastapi import params


class FilterParam(params.Query):  # noqa: N802
    """
    Custom query parameter class for filtering purposes.

    This class extends FastAPI's Query parameter class to provide
    additional functionality or custom behavior tailored for filtering.
    By default, it initializes with a None default value, but supports
    other keyword arguments that the parent Query class accepts.

    Parameters:
    -----------
    **kwargs :
        Additional keyword arguments supported by the parent Query class.
        For more details visit: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/

    Usage:
    ------
    Use as a dependency in FastAPI route functions to extract and
    process filtering parameters from the query string.

    Example:
    --------
    ```
    def get_items(filter: Optional[str] = FilterParam(...)):
        ...
    ```
    """

    def __init__(self, **kwargs: Any):
        super().__init__(None, **kwargs)
