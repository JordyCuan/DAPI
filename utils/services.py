from utils.database.repository import APIBaseModel, BaseRepository


class BaseService:
    def __init__(self, *, repository: BaseRepository):
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

    def destroy(self, *, id: int) -> None:  # TODO: Temporal. It has to be the response
        return self.repository.destroy(id=id)
