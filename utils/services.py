from typing import Protocol

from utils.database.repository import APIBaseModel, BaseRepository
from utils.filters import BaseFilterManager


class RepositoryProtocol(Protocol):  # pragma: no cover
    def retrieve_by_id(self, id=id) -> APIBaseModel:
        pass

    def retrieve(self, **filters) -> APIBaseModel:
        pass

    def set_filter_manager(self, filter_manager) -> None:
        pass

    def list(self, **filters) -> list[APIBaseModel]:
        pass

    def create(self, *, entity: dict) -> APIBaseModel:
        pass

    def update(self, *, id: int, entity: dict) -> APIBaseModel:
        pass

    def destroy(self, *, id: int) -> None:
        pass


class BaseService:
    def __init__(self, *, repository: RepositoryProtocol):
        self.repository = repository

    def get_by_id(self, *, id: int) -> APIBaseModel:
        return self.repository.retrieve_by_id(id=id)

    def get(self, **filters) -> APIBaseModel:
        return self.repository.retrieve(**filters)

    def list(self, filter_manager=None, **filters) -> list[APIBaseModel]:
        self.repository.set_filter_manager(filter_manager)
        return self.repository.list(**filters)

    def create(self, *, entity: dict) -> APIBaseModel:
        return self.repository.create(entity=entity)

    def update(self, *, id: int, entity: dict) -> APIBaseModel:
        return self.repository.update(id=id, entity=entity)

    def destroy(self, *, id: int):
        return self.repository.destroy(id=id)
