"""
schemas.py

This module defines data validation and serialization schemas using Pydantic.
These schemas are utilized for request and response data validation,
transformation, and documentation in the context of FastAPI or any other application
that requires structured data validation.

Currently, the module contains:

- `FilterSchema`: A schema to validate and process filter-related query parameters.

Usage:
------
These schemas can be imported and used in FastAPI route functions, models,
or other application components to validate, serialize, or deserialize data.

Example:
--------
```
from .schemas import FilterSchema

def process_data(filter: FilterSchema):
    ...
```

Note:
-----
When adding new schemas, ensure to provide necessary validations and documentation
for clarity and maintainability.
"""
from typing import Any, Optional, Type, TypeVar

from pydantic import BaseModel, ConfigDict, PrivateAttr, root_validator

T = TypeVar("T", bound="FilterSchema")


class FilterMeta:
    def __init__(self, options: Optional[dict[str, Any]] = None):
        self.model = getattr(options, "model", None)

        # NOTE: This is not used yet. WIP!
        # self.fields = getattr(options, "fields", None)
        # self.exclude = getattr(options, "exclude", None)
        # allowed_order_by_fields  # type: ignore
        # order_by_field_name


class FilterSchema(BaseModel):
    """
    Schema to validate and process filter-related query parameters.

    The schema checks the validity of filter attributes based on
    recognized "lookups" or operations (e.g., "gt", "lt", "eq", etc.)

    Attributes:
    -----------
    model_config : ConfigDict
        Configuration dictionary for the schema, forbidding extra
        attributes that are not explicitly defined.

    Methods:
    --------
    check_valid_filter_lookups:
        A root validator that checks the validity of filter attributes
        based on the recognized lookups.
    """

    model_config = ConfigDict(extra="forbid")
    _meta = PrivateAttr()

    def __new__(cls: Type[T], **kwargs: Optional[dict[str, Any]]) -> T:
        _meta = FilterMeta(getattr(cls, "Meta", None))
        new_class = super(FilterSchema, cls).__new__(cls)

        # Here (rather than __ini__) for better compatibility with validators
        cls._meta = _meta
        return new_class

    # def __init__(self, **data: Optional[dict[str, Any]]) -> None:
    #     super().__init__(**data)
    #     self._meta = FilterMeta(getattr(self, "Meta", None))

    # TODO: Validate ordering IF DEFINED

    # TODO: Possible bug? extra='forbid' is not working
    #       UPDATE: This is because of the nature of query params

    @root_validator(pre=True)
    def check_valid_filter_lookups(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        Validates filter attributes based on recognized lookups or operations.

        This validator checks if provided filter attributes are constructed
        with valid operations. Raises a ValueError for invalid attributes.

        Parameters:
        -----------
        values : dict
            Dictionary containing the provided filter attributes.

        Returns:
        --------
        dict
            The original dictionary if validation passes.

        Raises:
        -------
        ValueError:
            If any filter attribute is invalid.
        """

        valid_lookups = ["gt", "gte", "lt", "lte", "eq", "ieq", "contains", "icontains"]
        # TODO: valid_attrs = valid_lookups +
        for key in values.keys():
            if key.count("__") == 1:
                suffix = key.split("__")[-1]
                if suffix not in valid_lookups:
                    raise ValueError(
                        f"Filter attribute {key} should be a valid lookup: {', '.join(valid_lookups)}"
                    )
        return values
