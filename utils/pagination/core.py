from math import ceil
from typing import Any, Optional, Protocol

from sqlalchemy.orm import DeclarativeBase, Query


class PageNumberSchemaProtocol(Protocol):  # pragma: no cover
    page: Optional[int]
    page_size: Optional[int]


class LimitOffsetSchemaProtocol(Protocol):  # pragma: no cover
    limit: Optional[int]
    offset: Optional[int]


class BasePagination:
    def paginate_queryset(self, query: Query[DeclarativeBase]) -> Query[DeclarativeBase]:  # pragma: no cover
        raise NotImplementedError("paginate_queryset() must be implemented.")

    def get_paginated_response_data(self, results: list[dict[str, Any]]) -> dict[str, Any]:
        data: dict[str, Any] = {"data": results}
        if pagination := self.get_pagination_properties():
            data["pagination"] = pagination
        return data

    def get_pagination_properties(self) -> dict[str, Optional[int]]:  # pragma: no cover
        raise NotImplementedError("get_pagination_properties() must be implemented.")


class PageNumberPagination(BasePagination):
    count: int
    page: Optional[int]
    page_size: Optional[int]

    def __init__(self, schema: PageNumberSchemaProtocol) -> None:
        self.page = schema.page
        self.page_size = schema.page_size

    def paginate_queryset(self, query: Query[DeclarativeBase]) -> Query[DeclarativeBase]:
        if self.page and self.page_size:
            offset = (self.page - 1) * self.page_size
            query = query.limit(self.page_size).offset(offset)

        self.count = query.count()
        return query

    def get_pagination_properties(self) -> dict[str, Optional[int]]:
        # TODO: Consider adding `links` property/object to follow JSON API references.
        if self.page is None or self.page_size is None:
            return {}

        total_pages = int(ceil(self.count / float(self.page_size)))
        pagination_properties: dict[str, Optional[int]] = {
            "count": self.count,
            "page": self.page,
            "page_size": self.page_size,
            "previous_page": self.page - 1 if self.page > 1 else None,
            "total_pages": total_pages if total_pages else None,
            "next_page": self.page + 1 if self.page < total_pages else None,
        }
        return {prop: val for prop, val in pagination_properties.items() if val}


class LimitOffsetPagination(BasePagination):
    count: int
    offset: Optional[int]
    limit: Optional[int]

    def __init__(self, schema: LimitOffsetSchemaProtocol) -> None:
        self.offset = schema.offset
        self.limit = schema.limit

    def paginate_queryset(self, query: Query[DeclarativeBase]) -> Query[DeclarativeBase]:
        query = query.offset(self.offset).limit(self.limit)
        self.count = query.count()
        return query

    def get_pagination_properties(self) -> dict[str, Optional[int]]:
        # TODO: Consider adding `links` property/object to follow JSON API references.
        if self.offset is None and self.limit is None:
            return {}
        return {"count": self.count, "limit": self.limit, "offset": self.offset}
