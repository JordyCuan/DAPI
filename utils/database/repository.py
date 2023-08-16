from functools import wraps
from typing import Any, Callable, Dict, List, Type

from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from utils.database.models import APIBaseModel
from utils.exceptions import ImproperlyConfigured

# from utils.datetime import get_now_utc_datetime


class BaseRepository:
    model: Type[APIBaseModel]

    def __init__(self, *, session: Session):
        self.session = session

        for operation in self.apply_wrap_to():
            method = getattr(self, operation)
            setattr(self, operation, self.get_execution_wrapper(method))

    def get_model(self) -> Type[APIBaseModel]:
        if self.model is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a Model. Define %(cls)s.model, or override "
                "%(cls)s.get_model()." % {"cls": self.__class__.__name__}
            )
        return self.model

    # def get_by_id(self, *, id: int, ignore_deleted: bool = False) -> APIBaseModel:
    def get_by_id(self, *, id: int) -> APIBaseModel:
        filters: dict[str, Any] = {"id": id}
        # if ignore_deleted:
        #     filters["deleted_at"] = None  # TODO: Cohesion: Not all models could have this one
        return self.query_where(**filters).one()

    def get(self, **filters: Any) -> APIBaseModel:
        return self.query_where(**filters).one()

    def list(self, filter_manager=None, **filters: Any) -> List[APIBaseModel]:
        if filter_manager:
            return filter_manager.apply(self.session.query(self.model)).all()
        return self.query_where(**filters).all()

    def create(self, *, entity: Dict) -> APIBaseModel:
        new_record = self.model(**entity)
        self.session.add(new_record)
        return new_record

    def update(self, *, id: int, entity: Dict) -> APIBaseModel:
        # if "id" in entity and id != entity["id"]:
        if id != entity.pop("id", id):  # TODO: Handle it as http 422 code?
            # TODO: ValueError only works on exceptions raised by Pydantic. This one should be changed
            raise ValueError("ID in the entity does not match the given ID.")

        record = self.query_where(id=id)
        record.update(entity)
        return record.one()

    def destroy(self, *, id: int) -> APIBaseModel:
        record = self.get_by_id(id=id)  # ignore_deleted=False
        self.session.delete(record)
        return record

    # def soft_destroy(self, *, id: int) -> APIBaseModel:
    #     record = self.get_by_id(id=id)
    #     record.deleted_at = get_now_utc_datetime()  # TODO: Use overwrite?
    #     return record

    def apply_wrap_to(self) -> List[str]:
        return [
            "get_by_id",
            "get",
            "list",
            "create",
            "update",
            "destroy",
            # "soft_destroy"
        ]

    def get_execution_wrapper(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """This method encapsulates functionality that can be executed before and after each operation"""

        @wraps(func)
        def call(*args: Any, **kwargs: Any) -> Any:
            self.before_execution(func.__name__, *args, **kwargs)
            result = func(*args, **kwargs)
            self.session.flush()
            self.after_execution(
                func.__name__, *args, **kwargs
            )  # TODO: Or maybe return the result value from `after_execution`?
            return result

        return call

    def before_execution(self, method: str, *args: Any, **kwargs: Any) -> None:
        pass

    def after_execution(self, method: str, *args: Any, **kwargs: Any) -> None:
        if method in ["create", "update", "destroy", "soft_destroy"]:
            self.session.commit()

    def query_where(self, **filters: Any) -> Query:
        return self.session.query(self.model).filter_by(**filters)
