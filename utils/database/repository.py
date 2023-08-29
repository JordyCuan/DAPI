from typing import Any, Callable, Optional, Protocol, Type

from sqlalchemy.orm import DeclarativeBase, Query, Session

from utils.exceptions import ImproperlyConfigured


class FilterManagerProtocol(Protocol):  # pragma: no cover
    def filter_queryset(self, query: Query[DeclarativeBase]) -> Query[DeclarativeBase]:
        pass

    def order_by_queryset(self, query: Query[DeclarativeBase]) -> Query[DeclarativeBase]:
        pass


# class PaginationManagerProtocol(Protocol):
#     def paginate_queryset(self) -> Query:  # pragma: no cover
#         pass


class ListModelMixin:
    session: Session
    get_base_query: Callable[..., Query[DeclarativeBase]]
    filter_manager: Optional[FilterManagerProtocol] = None

    def list(self, **filters: Any) -> list[DeclarativeBase]:
        """
        Args:
            **filters: Filters to refine the query results.

        Returns:
            List of DeclarativeBase instances.
        """

        base_query = self.get_base_query()
        query = self.list_queryset(base_query, **filters)
        query = self.filter_queryset(query)
        query = self.order_by_queryset(query)
        return query.all()

    def list_queryset(self, base_query: Query[DeclarativeBase], **filters: Any) -> Query[DeclarativeBase]:
        """Override for custom list fetching logic."""
        return base_query.filter_by(**filters)

    def filter_queryset(self, query: Query[DeclarativeBase]) -> Query[DeclarativeBase]:
        """Override for custom filter logic."""
        if self.filter_manager:
            query = self.filter_manager.filter_queryset(query)
        return query

    def order_by_queryset(self, query: Query[DeclarativeBase]) -> Query[DeclarativeBase]:
        """Override for custom ordering logic."""
        if self.filter_manager:
            query = self.filter_manager.order_by_queryset(query)
        return query

    def paginate_queryset(self, query: Query[DeclarativeBase]) -> Query[DeclarativeBase]:
        """Override for custom pagination logic."""
        return query

    def set_filter_manager(self, filter_manager: FilterManagerProtocol) -> None:
        self.filter_manager = filter_manager  # NOTE: How to keep the repository stateless?

    # def set_pagination_manager(self, pagination_manager: PaginationManagerProtocol) -> None:
    #     if pagination_manager:
    #         setattr(self, "paginate_queryset", pagination_manager.filter_queryset)


class RetrieveModelMixin:
    session: Session
    get_base_query: Callable[..., Query[DeclarativeBase]]

    def retrieve_by_id(self, *, id: int) -> DeclarativeBase:
        """
        Args:
            id: ID of the entity to retrieve.

        Returns:
            Single DeclarativeBase instance.
        """
        base_query = self.get_base_query()
        return self.retrieve_queryset(base_query, id=id).one()

    def retrieve(self, **filters: Any) -> DeclarativeBase:
        """
        Args:
            **filters: Filters to refine the query results.

        Returns:
            Single DeclarativeBase instance.
        """
        base_query = self.get_base_query()
        return self.retrieve_queryset(base_query, **filters).one()

    def retrieve_queryset(self, base_query: Query[DeclarativeBase], **filters: Any) -> Query[DeclarativeBase]:
        """Override for custom retrieval logic."""
        return base_query.filter_by(**filters)


class CreateModelMixin:
    session: Session
    get_model: Callable[..., Type[DeclarativeBase]]

    def create(self, *, entity: dict[str, Any]) -> DeclarativeBase:
        """
        Args:
            entity: Data dictionary to create a new entity.

        Returns:
            Newly created DeclarativeBase instance.
        """
        model = self.get_model()
        new_record = self.create_queryset(model=model, entity=entity)
        self.session.add(new_record)
        self.session.flush()
        return new_record

    def create_queryset(self, *, model: Type[DeclarativeBase], entity: dict[str, Any]) -> DeclarativeBase:
        """Override for custom object creation logic."""
        return model(**entity)


class UpdateModelMixin:
    session: Session
    get_base_query: Callable[..., Query[DeclarativeBase]]

    def update(self, *, id: int, entity: dict[str, Any]) -> DeclarativeBase:
        """
        Args:
            id: ID of the entity to update.
            entity: Data dictionary with updated values.

        Returns:
            Updated DeclarativeBase instance.

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
        self, base_query: Query[DeclarativeBase], *, id: int, entity: dict[str, Any]
    ) -> Query[DeclarativeBase]:
        query = base_query.filter_by(id=id)
        query.update(entity)  # type: ignore[arg-type]
        return query


class DestroyModelMixin:
    session: Session
    get_base_query: Callable[..., Query[DeclarativeBase]]

    def destroy(self, *, id: int) -> None:
        """
        Args:
            id: ID of the entity to delete.
        """
        base_query = self.get_base_query()
        instance = self.destroy_queryset(base_query, id=id).one()
        self.perform_destroy(instance)
        self.session.flush()

    def destroy_queryset(self, base_query: Query[DeclarativeBase], *, id: int) -> Query[DeclarativeBase]:
        query = base_query.filter_by(id=id)
        return query

    def perform_destroy(self, instance: DeclarativeBase) -> None:
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
    model: Optional[Type[DeclarativeBase]]

    def __init__(self, *, session: Session):
        """
        Args:
            session: SQLAlchemy session instance.
        """
        self.session = session

    def get_model(self) -> Type[DeclarativeBase]:
        """Get the model associated with this repository. Raise exception if not set."""
        if self.model is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a Model. Define %(cls)s.model, or override "
                "%(cls)s.get_model()." % {"cls": self.__class__.__name__}
            )
        return self.model

    def get_base_query(self) -> Query[DeclarativeBase]:
        """Provides the base query associated with the model of the repository."""
        return self.session.query(self.get_model())

    def perform_commit(self) -> None:
        self.session.commit()
