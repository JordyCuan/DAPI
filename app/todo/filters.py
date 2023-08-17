from typing import List, Optional

from utils.filters import BaseFilterManager, FilterParam, FilterSchema

from .models import Todo


class TodoFilterSchema(FilterSchema):
    title__ieq: Optional[str] = FilterParam()
    priority__gt: Optional[int] = FilterParam()
    priority__gte: Optional[int] = FilterParam()
    priority__lt: Optional[int] = FilterParam()
    priority__lte: Optional[int] = FilterParam()
    priority__eq: Optional[int] = FilterParam()
    complete__eq: Optional[bool] = FilterParam()
    description__contains: Optional[str] = FilterParam()
    description__icontains: Optional[str] = FilterParam()
    # title__in: list[str] = FilterParam()  # TODO: But then, how to gather the elements to get the Query?
    # ordering: List[str] = FilterParam()  # TODO: 1. Bug. 2.Let's fine a way to set a customizable field.


class TodoFilterManager(BaseFilterManager):
    model = Todo
