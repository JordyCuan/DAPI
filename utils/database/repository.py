from typing import Any, Callable, Generic, Optional, Protocol, Type, TypeVar

from sqlalchemy.orm import DeclarativeBase, Query, Session

from utils.exceptions import ImproperlyConfigured

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class FilterManagerProtocol(Protocol):  # pragma: no cover
    def filter_queryset(self, query: Query[ModelType]) -> Query[ModelType]:
        pass

    def order_by_queryset(self, query: Query[ModelType]) -> Query[ModelType]:
        pass


class PaginationManagerProtocol(Protocol):  # pragma: no cover
    def paginate_queryset(self, query: Query[ModelType]) -> Query[ModelType]:
        pass


class ListModelMixin(Generic[ModelType]):
    session: Session
    get_base_query: Callable[..., Query[ModelType]]

    def list(
        self,
        *,
        filter_manager: Optional[FilterManagerProtocol] = None,
        pagination_manager: Optional[PaginationManagerProtocol] = None,
        **filters: Any,
    ) -> list[ModelType]:
        """
        Args:
            filter_manager: Object implementing `filter_queryset` and `order_by_queryset` methods
            pagination_manager: Object implementing `paginate_queryset` method
            **filters: Filters to refine the query results.

        Returns:
            List of ModelType instances.
        """

        base_query = self.get_base_query()
        query = self.list_queryset(base_query, **filters)
        if filter_manager:
            query = filter_manager.filter_queryset(query)
            query = filter_manager.order_by_queryset(query)
        if pagination_manager:
            query = pagination_manager.paginate_queryset(query)
        return query.all()

    def list_queryset(self, base_query: Query[ModelType], **filters: Any) -> Query[ModelType]:
        """Override for custom list fetching logic."""
        return base_query.filter_by(**filters)


class RetrieveModelMixin(Generic[ModelType]):
    session: Session
    get_base_query: Callable[..., Query[ModelType]]

    def retrieve_by_id(self, *, id: int) -> ModelType:
        """
        Args:
            id: ID of the entity to retrieve.

        Returns:
            Single ModelType instance.
        """
        base_query = self.get_base_query()
        return self.retrieve_queryset(base_query, id=id).one()

    def retrieve(self, **filters: Any) -> ModelType:
        """
        Args:
            **filters: Filters to refine the query results.

        Returns:
            Single ModelType instance.
        """
        base_query = self.get_base_query()
        return self.retrieve_queryset(base_query, **filters).one()

    def retrieve_queryset(self, base_query: Query[ModelType], **filters: Any) -> Query[ModelType]:
        """Override for custom retrieval logic."""
        return base_query.filter_by(**filters)


class CreateModelMixin(Generic[ModelType]):
    session: Session
    get_model: Callable[..., Type[ModelType]]

    def create(self, *, entity: dict[str, Any]) -> ModelType:
        """
        Args:
            entity: Data dictionary to create a new entity.

        Returns:
            Newly created ModelType instance.
        """
        model = self.get_model()
        new_record = self.create_queryset(model=model, entity=entity)
        self.session.add(new_record)
        self.session.flush()
        return new_record

    def create_queryset(self, *, model: Type[ModelType], entity: dict[str, Any]) -> ModelType:
        """Override for custom object creation logic."""
        return model(**entity)


class UpdateModelMixin(Generic[ModelType]):
    session: Session
    get_base_query: Callable[..., Query[ModelType]]

    def update(self, *, id: int, entity: dict[str, Any]) -> ModelType:
        """
        Args:
            id: ID of the entity to update.
            entity: Data dictionary with updated values.

        Returns:
            Updated ModelType instance.

        Raises:
            ValueError: If provided ID doesn't match entity's ID.
        """
        if id != entity.pop("id", id):
            raise ValueError("ID in the entity does not match the given ID.")

        base_query = self.get_base_query()
        query = self.update_queryset(base_query, id=id, entity=entity)
        instance = query.one()
        self.session.flush()
        return instance

    def update_queryset(
        self, base_query: Query[ModelType], *, id: int, entity: dict[str, Any]
    ) -> Query[ModelType]:
        query = base_query.filter_by(id=id)
        query.update(entity)  # type: ignore[arg-type]
        return query


class DestroyModelMixin(Generic[ModelType]):
    session: Session
    get_base_query: Callable[..., Query[ModelType]]

    def destroy(self, *, id: int) -> None:
        """
        Args:
            id: ID of the entity to delete.
        """
        base_query = self.get_base_query()
        instance = self.destroy_queryset(base_query, id=id).one()
        self.perform_destroy(instance)
        self.session.flush()

    def destroy_queryset(self, base_query: Query[ModelType], *, id: int) -> Query[ModelType]:
        query = base_query.filter_by(id=id)
        return query

    def perform_destroy(self, instance: ModelType) -> None:
        """
        Handle deletion of an instance. Override for custom delete behavior, e.g., soft deletes.
        In case of soft-delete this method can be easily overwritten and
        set it as `instance.deleted_at = now()`
        """
        self.session.delete(instance)


class BaseRepository(
    ListModelMixin[ModelType],
    RetrieveModelMixin[ModelType],
    CreateModelMixin[ModelType],
    UpdateModelMixin[ModelType],
    DestroyModelMixin[ModelType],
):
    model: Optional[Type[ModelType]]

    def __init__(self, *, session: Session):
        """
        Args:
            session: SQLAlchemy session instance.
        """
        self.session = session

    def get_model(self) -> Type[ModelType]:
        """Get the model associated with this repository. Raise exception if not set."""
        if self.model is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a Model. Define %(cls)s.model, or override "
                "%(cls)s.get_model()." % {"cls": self.__class__.__name__}
            )
        return self.model

    def get_base_query(self) -> Query[ModelType]:
        """Provides the base query associated with the model of the repository."""
        return self.session.query(self.get_model())

    def perform_commit(self) -> None:
        self.session.commit()
