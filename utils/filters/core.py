from typing import Any, Callable, Dict, Optional, Type

from sqlalchemy import and_, asc, desc
from sqlalchemy.orm import DeclarativeBase, Query

from .schemas import FilterSchema


class BaseFilterManager:
    """
    The BaseFilterManager provides a mapping of operation names to filtering
    functions for the specified SQL model.

    Attributes:
    -----------
    model : Type[DeclarativeBase]
        The SQL model to be filtered.

    OPERATIONS : Dict[str, Callable[[Any, Any], Any]]
        A dictionary mapping operation names to lambda functions that
        perform the operation using the provided column and value.

    filters : dict
        Contains filters specified as key-value pairs, where keys can have
        operation postfixes (e.g., "field__op").

    ordering : Optional[list[str]]
        List of fields by which the queryset should be ordered.

    Available operations:
    ---------------------
    - "gt": Greater than
    - "gte": Greater than or equal to
    - "lt": Less than
    - "lte": Less than or equal to
    - "eq": Equal to
    - "ieq": Case insensitive equality (using `ILIKE`)
    - "contains": Check if column contains the value
    - "icontains": Case insensitive check if column contains the value

    Example:
    --------
    TODO:
    if "gt" operation is selected, the lambda function will evaluate if
    the specified column's value is greater than the provided value.

    Usage:
    ------
    TODO:
    For using the operations, directly access the OPERATIONS dictionary
    with the desired operation name as the key.
    """

    model: Type[DeclarativeBase]

    OPERATIONS: Dict[str, Callable[[Any, Any], Any]] = {
        "gt": lambda col, val: col > val,
        "gte": lambda col, val: col >= val,
        "lt": lambda col, val: col < val,
        "lte": lambda col, val: col <= val,
        "eq": lambda col, val: col == val,
        "ieq": lambda col, val: col.ilike(val),
        "contains": lambda col, val: col.contains(val),
        "icontains": lambda col, val: col.ilike(f"%{val}%"),
    }

    def __init__(self, *, filters: Type[FilterSchema]) -> None:
        """
        Parameters:
        -----------
        filters : Type[FilterSchema]
            A schema containing filtering conditions.
            See `filters.schemas.FilterSchema` for more details.
        """
        self.filters = filters.model_dump(exclude_none=True, exclude_unset=True)  # type: ignore

        # TODO: How to define `ordering`
        self.ordering: Optional[list[str]] = getattr(self.filters, "ordering", None)

    def filter_queryset(self, query: Query) -> Query:
        """
        Applies filtering conditions from self.filters to the provided query.

        Parameters:
        -----------
        query : Query
            The query to be filtered.

        Returns:
        --------
        Query
            The filtered query.
        """
        if self.filters is None:
            return query
        conditions = []
        for key, value in self.filters.items():
            if "__" in key:
                field, op = key.split("__")
                column = getattr(self.model, field)
                conditions.append(self.OPERATIONS[op](column, value))
        return query.filter(and_(*conditions))

    def order_by_queryset(self, query: Query) -> Query:
        """
        Orders the provided query based on self.ordering.

        Parameters:
        -----------
        query : Query
            The query to be ordered.

        Returns:
        --------
        Query
            The ordered query.
        """
        if self.ordering is None:
            return query
        for order in self.ordering:
            if order.startswith("-"):
                query = query.order_by(desc(getattr(self.model, order[1:])))
            else:
                query = query.order_by(asc(getattr(self.model, order)))
        return query

    def paginate_queryset(self, query: Query) -> Query:
        # TODO: Implement this feature. Is it a part of this?
        return query
        # return query.offset((page - 1) * page_size).limit(page_size)
