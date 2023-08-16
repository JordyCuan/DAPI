from typing import Any, Callable, Dict, List, Optional, Type

from sqlalchemy.orm import Query, Session

from utils.database.models import APIBaseModel
from utils.exceptions import ImproperlyConfigured


class ListModelMixin:
    session: Session
    get_base_query: Callable[..., Query]

    # TODO: FilterManager?
    def list(self, filter_manager: Optional[Any] = None, **filters: Any) -> List[APIBaseModel]:
        """
        Args:
            filter_manager: An optional manager for custom filtering.
            **filters: Filters to refine the query results.

        Returns:
            List of APIBaseModel instances.
        """
        base_query = self.get_base_query()
        return self.list_queryset(base_query, filter_manager=filter_manager, **filters).all()

    def list_queryset(
        self, base_query: Query, *, filter_manager: Optional[Any] = None, **filters: Any
    ) -> Query:
        """Override for custom list fetching logic."""
        return base_query.filter_by(**filters)

    def filter_queryset(self, query: Query) -> Query:
        """Override for custom filter logic."""
        return query

    def order_by_queryset(self, query: Query) -> Query:
        """Override for custom ordering logic."""
        return query

    def paginate_queryset(self, query: Query) -> Query:
        """Override for custom pagination logic."""
        return query


class RetrieveModelMixin:
    session: Session
    get_base_query: Callable[..., Query]

    def retrieve_by_id(self, *, id: int) -> APIBaseModel:
        """
        Args:
            id: ID of the entity to retrieve.

        Returns:
            Single APIBaseModel instance.
        """
        base_query = self.get_base_query()
        return self.retrieve_queryset(base_query, id=id).one()

    def retrieve(self, **filters: Any) -> APIBaseModel:
        """
        Args:
            **filters: Filters to refine the query results.

        Returns:
            Single APIBaseModel instance.
        """
        base_query = self.get_base_query()
        return self.retrieve_queryset(base_query, **filters).one()

    def retrieve_queryset(self, base_query: Query, **filters: Any) -> Query:
        """Override for custom retrieval logic."""
        return base_query.filter_by(**filters)


class CreateModelMixin:
    session: Session
    get_model: Callable[..., Type[APIBaseModel]]

    def create(self, *, entity: Dict) -> APIBaseModel:
        """
        Args:
            entity: Data dictionary to create a new entity.

        Returns:
            Newly created APIBaseModel instance.
        """
        model = self.get_model()
        new_record = self.create_queryset(model=model, entity=entity)
        self.session.add(new_record)
        self.session.flush()
        return new_record

    def create_queryset(self, *, model: Type[APIBaseModel], entity: Dict) -> APIBaseModel:
        """Override for custom object creation logic."""
        return model(**entity)


class UpdateModelMixin:
    session: Session
    get_base_query: Callable[..., Query]

    def update(self, *, id: int, entity: Dict) -> APIBaseModel:
        """
        Args:
            id: ID of the entity to update.
            entity: Data dictionary with updated values.

        Returns:
            Updated APIBaseModel instance.

        Raises:
            ValueError: If provided ID doesn't match entity's ID.
        """
        # TODO: Popping? References elsewhere?
        if id != entity.pop("id", id):
            raise ValueError("ID in the entity does not match the given ID.")

        base_query = self.get_base_query()
        query = self.update_queryset(base_query, id=id, entity=entity)
        self.session.flush()
        return query.one()

    def update_queryset(self, base_query: Query, *, id: int, entity: Dict) -> Query:
        query = base_query.filter_by(id=id)
        assert query.count() == 1, "Update on non existing entry or multiple entries found"
        query.update(entity)
        return query


class DestroyModelMixin:
    session: Session
    get_base_query: Callable[..., Query]

    def destroy(self, *, id: int) -> None:
        """
        Args:
            id: ID of the entity to delete.
        """
        base_query = self.get_base_query()
        instance = self.destroy_queryset(base_query, id=id).one()
        self.perform_destroy(instance)
        self.session.flush()

    def destroy_queryset(self, base_query: Query, *, id: int) -> Query:
        query = base_query.filter_by(id=id)
        assert query.count() == 1, "Update on non existing entry or multiple entries found"
        return query

    def perform_destroy(self, instance: Type[APIBaseModel]):
        """
        Handle deletion of an instance. Override for custom delete behavior, e.g., soft deletes.
        In case of soft-delete this method can be easily overwritten and
        set it as `instance.deleted_at = now()`
        """
        self.session.delete(instance)


class BaseRepository(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    model: Type[APIBaseModel]

    def __init__(self, *, session: Session):
        """
        Args:
            session: SQLAlchemy session instance.
        """
        self.session = session

    def get_model(self) -> Type[APIBaseModel]:
        """Get the model associated with this repository. Raise exception if not set."""
        if self.model is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a Model. Define %(cls)s.model, or override "
                "%(cls)s.get_model()." % {"cls": self.__class__.__name__}
            )
        return self.model

    def get_base_query(self) -> Query[APIBaseModel]:
        """Provides the base query associated with the model of the repository."""
        return self.session.query(self.get_model())

    def perform_commit(self):
        self.session.commit()
