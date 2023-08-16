from typing import Any, Callable, Dict, List, Optional, Type

from pydantic import BaseModel, ConfigDict, Extra, root_validator
from sqlalchemy import and_, asc, desc
from sqlalchemy.orm import Query

from utils.database.repository import APIBaseModel


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
