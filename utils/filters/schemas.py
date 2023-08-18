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
from pydantic import BaseModel, ConfigDict, Extra, root_validator


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

    model_config = ConfigDict(extra=Extra.forbid)

    @root_validator(pre=True)
    def check_valid_filter_lookups(cls, values):
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
        valid_lookups = ["gt", "gte", "lt", "lte", "eq", "ieq", "contains", "icontains", "ordering"]
        for key in values.keys():
            if key.count("__") == 1:
                suffix = key.split("__")[-1]
                if suffix not in valid_lookups:
                    raise ValueError(
                        f"Filter attribute {key} should be a valid lookup: {', '.join(valid_lookups)}"
                    )
        return values


# class PaginationParams(BaseModel):
#     page: Optional[int] = Field(1, gt=0)
#     page_size: Optional[int] = Field(10, gt=0, le=100)


# class FilterParams(BaseModel):
#     filters: Optional[Dict[str, Any]]


# class OrderParams(BaseModel):
#     orders: Optional[List[str]]
