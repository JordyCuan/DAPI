"""
param_functions.py

This module provides functional wrappers around parameter classes defined in the `params` module.
These functions allow for more flexible and concise usage patterns when integrating with
FastAPI route functions or other application components.

Currently, this module contains the following functions:

- `FilterParam`: A functional wrapper around the `FilterParam` class from the `params` module.

Usage:
------
These functions can be imported and used as dependencies in FastAPI route functions
to extract and process different parameters from the query string or other parts
of the HTTP request, offering a streamlined way to utilize custom parameter classes.

Example:
--------
```
from .param_functions import FilterParam

@app.get("/items/")
def get_items(filter: FilterParam(...)):  # TODO
    ...
```

Note:
-----
For more details visit: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/
"""
from typing import Any

from . import params


def FilterParam(**kwargs: Any) -> Any:  # noqa: N802
    """
    Functional wrapper around the `FilterParam` class from the `filters.params` module.

    This function offers a more concise way to utilize the `FilterParam` class by
    allowing direct invocation without the need to instantiate the class explicitly.

    Parameters:
    -----------
    **kwargs :
        Keyword arguments supported by the `FilterParam` class in the `filters.params` module.
        For more details visit: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/

    Returns:
    --------
    params.FilterParam
        An instance of the `filters.params.FilterParam` class initialized with the provided keyword arguments.
    """
    return params.FilterParam(**kwargs)
