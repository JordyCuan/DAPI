from typing import Optional

from utils.filters import BaseFilterManager, BaseFilterSchema

from .models import Todo


class TodoFilterSchema(BaseFilterSchema):
    title__ieq: Optional[str]
    priority__gt: Optional[int]
    priority__gte: Optional[int]
    priority__lt: Optional[int]
    priority__lte: Optional[int]
    priority__eq: Optional[int]
    complete__eq: Optional[bool]
    description__contains: Optional[str]
    description__icontains: Optional[str]


class TodoFilterManager(BaseFilterManager):
    model = Todo
