from typing import Any, Dict, List, Optional, Union

from sqlalchemy import Column, and_, asc, between, desc, or_


class BaseFilter:
    fields: Union[Dict[str, List[str]], List[str]] = []

    def __init__(self, model):
        self.model = model

    def filter_query(self, query, filters: Optional[Dict[str, Any]]):
        if filters is None:
            return query
        conditions = []
        for key, value in filters.items():
            if "__" in key:
                field, op = key.split("__")
                # Ensure the field is allowed to be filtered
                if not self.is_filterable(field, op):
                    continue
                column = getattr(self.model, field)
                if op == "gt":
                    conditions.append(column > value)
                elif op == "gte":
                    conditions.append(column >= value)
                elif op == "lt":
                    conditions.append(column < value)
                elif op == "lte":
                    conditions.append(column <= value)
                elif op == "eq":
                    conditions.append(column == value)
                elif op == "ci_eq":  # Case insensitive equals
                    conditions.append(column.ilike(value))
                elif op == "contains":
                    conditions.append(column.contains(value))
                elif op == "ci_contains":  # Case insensitive contains
                    conditions.append(column.ilike(f"%{value}%"))
                elif op == "isnull":
                    conditions.append(column.is_(None) if value else column.isnot(None))
                elif op == "range":
                    if isinstance(value, list) and len(value) == 2:
                        conditions.append(column.between(value[0], value[1]))
                # TODO: handle more operators as required
            else:
                conditions.append(getattr(self.model, key) == value)
        return query.filter(and_(*conditions))

    def order_query(self, query, orders: Optional[List[str]]):
        if orders is None:
            return query
        for order in orders:
            if order.startswith("-"):
                query = query.order_by(desc(getattr(self.model, order[1:])))
            else:
                query = query.order_by(asc(getattr(self.model, order)))
        return query

    def paginate_query(self, query, page: int, page_size: int):
        return query.offset((page - 1) * page_size).limit(page_size)

    def apply(
        self,
        query,
        filters: Optional[Dict[str, Any]],
        orders: Optional[List[str]],
        page: int = 1,
        page_size: int = 10,
    ):
        return self.paginate_query(
            self.order_query(self.filter_query(query, filters), orders), page, page_size
        )

    def is_filterable(self, field: str, op: str) -> bool:
        if isinstance(self.fields, list):
            return field in self.fields
        elif isinstance(self.fields, dict):
            return field in self.fields and op in self.fields[field]
        return False
