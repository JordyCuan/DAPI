from typing import Annotated, Optional

from fastapi import Query

from utils.filters import BaseFilterManager, FilterSchema

from .models import Todo


class TodoFilterSchema(FilterSchema, extra="forbid"):
    title__ieq: Optional[str] = Query(None)
    priority__gt: Optional[int] = Query(None)
    priority__gte: Optional[int] = Query(None)
    priority__lt: Optional[int] = Query(None)
    priority__lte: Optional[int] = Query(None)
    priority__eq: Optional[int] = Query(None)
    complete__eq: Optional[bool] = Query(None)
    description__contains: Annotated[str | None, Query(None)]
    description__icontains: Optional[str] = Query(None)

    # Annotated[str | None, Query(None)]
    # title__in: list[str] = Query(None)  # TODO: But then, how to gather the elements to get the Query?

    # NOTE: When List[] = Query() param is an inner object it is NOT threated as query param but Body()
    # ordering: Optional[List[str]] = Query(None)
    # ordering: List[int] = Query(None)
    # ordering: Annotated[list[str] | None, Query()] = None

    # class Meta:
    #     model = Todo


class TodoFilterManager(BaseFilterManager):
    model = Todo
