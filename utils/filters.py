from typing import Any, Callable, Dict, List, Optional, Type, Union

from pydantic import BaseModel, ConfigDict, Extra, root_validator
from sqlalchemy import Column, and_, asc, between, desc, or_
from sqlalchemy.orm import MappedColumn, Query

from utils.database.repository import APIBaseModel
from utils.exceptions import ImproperlyConfigured


class BaseFilterSchema(BaseModel):
    model_config = ConfigDict(extra=Extra.forbid)

    @root_validator(pre=True)
    def check_valid_filter_lookups(cls, values):
        valid_lookups = ["gt", "gte", "lt", "lte", "eq", "ieq", "contains", "icontains"]
        for key in values.keys():
            if key.count("__") == 1:
                suffix = key.split("__")[-1]
                if suffix not in valid_lookups:
                    raise ValueError(
                        f"Filter attribute {key} should be a valid lookup: {', '.join(valid_lookups)}"
                    )
        return values


class BaseFilterManager:
    model: Type[APIBaseModel]

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

    def __init__(self, *, filters: BaseFilterSchema) -> None:
        self.filters = filters.model_dump(exclude_none=True, exclude_unset=True)  # type: ignore

    def filter(self, query: Query) -> Query:
        if self.filters is None:
            return query
        conditions = []
        for key, value in self.filters.items():
            if "__" in key:
                field, op = key.split("__")
                column = getattr(self.model, field)
                conditions.append(self.OPERATIONS[op](column, value))
        return query.filter(and_(*conditions))

    def order_by(self, query: Query, orders: Optional[List[str]] = None) -> Query:
        if orders is None:
            return query
        for order in orders:
            if order.startswith("-"):
                query = query.order_by(desc(getattr(self.model, order[1:])))
            else:
                query = query.order_by(asc(getattr(self.model, order)))
        return query

    # def paginate(self, query: Query, page: int = 1, page_size: int = 10) -> Query:
    #     return query.offset((page - 1) * page_size).limit(page_size)

    def apply(
        self,
        query: Query,
        # page: Optional[int] = None,
        # page_size: Optional[int] = None,
    ) -> Query:
        new_query = self.filter(query)
        new_query = self.order_by(new_query)
        # if page and page_size:
        #     return self.paginate(new_query, page, page_size)
        return new_query


# class BaseFilterManager:
#     model: Type[APIBaseModel]

#     def __init__(self, filters: Dict[str, Any]) -> None:
#         self.filters = filters

#     def filter(self, query, filters: Optional[Dict[str, Any]]):
#         if filters is None:
#             return query
#         conditions = []
#         for key, value in filters.items():
#             if "__" in key:
#                 field, op = key.split("__")
#                 if not self.is_filterable(field, op):
#                     continue
#                 column = getattr(self.model, field)
#                 if op == "gt":
#                     conditions.append(column > value)
#                 elif op == "gte":
#                     conditions.append(column >= value)
#                 elif op == "lt":
#                     conditions.append(column < value)
#                 elif op == "lte":
#                     conditions.append(column <= value)
#                 elif op == "eq":
#                     conditions.append(column == value)
#                 elif op == "ieq":  # Case insensitive equals
#                     conditions.append(column.ilike(value))
#                 elif op == "contains":
#                     conditions.append(column.contains(value))
#                 elif op == "icontains":  # Case insensitive contains
#                     conditions.append(column.ilike(f"%{value}%"))
#                 elif op == "isnull":
#                     conditions.append(column.is_(None) if value else column.isnot(None))
#             else:
#                 conditions.append(getattr(self.model, key) == value)
#         return query.filter(and_(*conditions))

#     def order(self, query, orders: Optional[List[str]]):
#         if orders is None:
#             return query
#         for order in orders:
#             if order.startswith("-"):
#                 query = query.order_by(desc(getattr(self.model, order[1:])))
#             else:
#                 query = query.order_by(asc(getattr(self.model, order)))
#         return query

#     def paginate(self, query, page: int, page_size: int):
#         return query.offset((page - 1) * page_size).limit(page_size)

#     def apply(
#         self,
#         query,
#         filters: Optional[Dict[str, Any]],
#         orders: Optional[List[str]],
#         page: int = 1,
#         page_size: int = 10,
#     ):
#         return self.paginate_query(
#             self.order_by(self.filter_query(query, filters), orders), page, page_size
#         )

#     def is_filterable(self, field: str, op: str) -> bool:
#         return field in self._fields and op in self._fields[field]
