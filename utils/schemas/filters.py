from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: Optional[int] = Field(1, gt=0)
    page_size: Optional[int] = Field(10, gt=0, le=100)


class FilterParams(BaseModel):
    filters: Optional[Dict[str, Any]]


class OrderParams(BaseModel):
    orders: Optional[List[str]]
