from typing import Any, Optional, Protocol

from sqlalchemy.orm import DeclarativeBase

from .database.repository import FilterManagerProtocol, PaginationManagerProtocol


class RepositoryProtocol(Protocol):  # pragma: no cover
    def retrieve_by_id(self, *, id: int) -> DeclarativeBase:
        pass

    def retrieve(self, **filters: Any) -> DeclarativeBase:
        pass

    def list(
        self,
        *,
        filter_manager: Optional[FilterManagerProtocol] = None,
        pagination_manager: Optional[PaginationManagerProtocol] = None,
        **filters: Any,
    ) -> list[DeclarativeBase]:
        pass

    def create(self, *, entity: dict[str, Any]) -> DeclarativeBase:
        pass

    def update(self, *, id: int, entity: dict[str, Any]) -> DeclarativeBase:
        pass

    def destroy(self, *, id: int) -> None:
        pass


class BaseService:
    def __init__(self, *, repository: RepositoryProtocol):
        self.repository = repository

    def get_by_id(self, *, id: int) -> DeclarativeBase:
        return self.repository.retrieve_by_id(id=id)

    def get(self, **filters: Any) -> DeclarativeBase:
        return self.repository.retrieve(**filters)

    def list(
        self,
        filter_manager: Optional[FilterManagerProtocol] = None,
        pagination_manager: Optional[PaginationManagerProtocol] = None,
        **filters: Any,
    ) -> list[DeclarativeBase]:
        return self.repository.list(
            filter_manager=filter_manager, pagination_manager=pagination_manager, **filters
        )

    def create(self, *, entity: dict[str, Any]) -> DeclarativeBase:
        return self.repository.create(entity=entity)

    def update(self, *, id: int, entity: dict[str, Any]) -> DeclarativeBase:
        return self.repository.update(id=id, entity=entity)

    def destroy(self, *, id: int) -> None:
        return self.repository.destroy(id=id)
