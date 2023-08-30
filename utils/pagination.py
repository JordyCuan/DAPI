from typing import Any, Optional

from fastapi import param_functions
from pydantic import BaseModel, model_validator
from sqlalchemy.orm import DeclarativeBase, Query
from starlette.responses import JSONResponse


class PageNumberSchema(BaseModel):
    page: Optional[int] = param_functions.Query(None, gt=0)
    page_size: Optional[int] = param_functions.Query(None, gt=0, le=100)


class LimitOffsetSchema(BaseModel):
    limit: Optional[int] = param_functions.Query(None, gt=0)
    offset: Optional[int] = param_functions.Query(None, gt=0, le=100)

    @model_validator(mode="before")
    @classmethod
    def check_both_fields_set(cls, values: dict[str, Any]) -> dict[str, Any]:
        limit = values.get("limit")
        offset = values.get("offset")
        if limit is None and offset:
            raise ValueError("Attribute `offset` should be along `limit`.")
        return values


class BasePagination:
    def paginate_queryset(self, query: Query[DeclarativeBase]) -> Query[DeclarativeBase]:  # pragma: no cover
        raise NotImplementedError("paginate_queryset() must be implemented.")

    # TODO: Is it really a response or must it be a dict?
    def get_paginated_response(self, data: dict[str, Any]) -> JSONResponse:  # pragma: no cover
        raise NotImplementedError("get_paginated_response() must be implemented.")


class PageNumberPagination(BasePagination):  # pragma: no cover
    # NOTE: WIP
    max_page_size = None


class LimitOffsetPagination(BasePagination):
    offset: Optional[int]
    limit: Optional[int]
    count: Optional[int]

    def __init__(self, schema: LimitOffsetSchema) -> None:
        self.offset = schema.offset
        self.limit = schema.limit

    def paginate_queryset(self, query: Query[DeclarativeBase]) -> Query[DeclarativeBase]:
        query = query.offset(self.offset).limit(self.limit)
        self.count = query.count()
        return query

    def get_paginated_response(self, data: dict[str, Any]) -> JSONResponse:
        return JSONResponse(
            {
                "count": self.count,
                "results": data,
                # "links": {
                #     "next": "http://api.example.com/items/?limit=10&offset=20",
                #     "previous": "http://api.example.com/items/?limit=10"
                # },
            }
        )
