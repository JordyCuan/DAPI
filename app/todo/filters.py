from typing import Annotated, Optional

from utils.filters import BaseFilterManager, FilterParam, FilterSchema

from .models import Todo

# from sqlalchemy.orm import Query
# from fastapi import Query


class TodoFilterSchema(FilterSchema, extra="forbid"):
    title__ieq: Optional[str] = FilterParam()
    priority__gt: Optional[int] = FilterParam()
    priority__gte: Optional[int] = FilterParam()
    priority__lt: Optional[int] = FilterParam()
    priority__lte: Optional[int] = FilterParam()
    priority__eq: Optional[int] = FilterParam()
    complete__eq: Optional[bool] = FilterParam()
    description__contains: Annotated[str | None, FilterParam()]
    description__icontains: Optional[str] = FilterParam()

    # Annotated[str | None, FilterParam()]
    # title__in: list[str] = FilterParam()  # TODO: But then, how to gather the elements to get the Query?

    # NOTE: When List[] = Query() param is an inner object it is NOT threated as query param but Body()
    # ordering: Optional[List[str]] = FilterParam()
    # ordering: List[int] = Query(None)
    # ordering: Annotated[list[str] | None, Query()] = None

    # class Meta:
    #     model = Todo


class TodoFilterManager(BaseFilterManager):
    model = Todo
