from typing import Any, Optional

from fastapi import param_functions
from pydantic import BaseModel, model_validator

MAX_PAGE_SIZE = 100


class PageNumberSchema(BaseModel):
    page: Optional[int] = param_functions.Query(None, gt=0, description="Page current location", alias="p")
    page_size: Optional[int] = param_functions.Query(
        None, gt=0, le=MAX_PAGE_SIZE, description="Page size fetched elements", alias="s"
    )

    @model_validator(mode="before")
    @classmethod
    def check_both_fields_set(cls, values: dict[str, Any]) -> dict[str, Any]:
        page = values.get("page")
        page_size = values.get("page_size")
        if (page is None and page_size) or (page_size is None and page):
            raise ValueError("Attributes `page` and `page_size` should be either declared or omitted.")
        return values


class LimitOffsetSchema(BaseModel):
    limit: Optional[int] = param_functions.Query(
        None, gt=0, le=MAX_PAGE_SIZE, description="Limit selection", alias="l"
    )
    offset: Optional[int] = param_functions.Query(None, gt=0, description="Offset selection", alias="o")

    @model_validator(mode="before")
    @classmethod
    def check_both_fields_set(cls, values: dict[str, Any]) -> dict[str, Any]:
        limit = values.get("limit")
        offset = values.get("offset")
        if (limit is None and offset) or (offset is None and limit):
            raise ValueError("Attributes `limit` and `offset` should be either declared or omitted.")
        return values
