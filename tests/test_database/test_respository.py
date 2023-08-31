from unittest.mock import MagicMock

import pytest
from sqlalchemy import Column, String
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from utils.database.models import APIBaseModel
from utils.database.repository import BaseRepository
from utils.exceptions.generic import ImproperlyConfigured


class MockModel(APIBaseModel):
    name = Column(String)


class TestBaseRepository:
    @pytest.fixture(autouse=True)
    def setup_class(self, session: Session) -> None:
        self.session = session
        self.repository = BaseRepository(session=session)
        self.repository.model = MockModel

    def test_get_model(self) -> None:
        assert self.repository.get_model() == MockModel

        self.repository.model = None
        with pytest.raises(ImproperlyConfigured):
            self.repository.get_model()

    def test_create(self) -> None:
        entity = {"id": 1, "name": "Test"}
        self.repository.create(entity=entity)

        created_entity = self.session.query(MockModel).first()
        assert created_entity.id == 1  # type: ignore
        assert created_entity.name == "Test"  # type: ignore

        with pytest.raises(IntegrityError):
            self.repository.create(entity=entity)

    def test_retrieve_by_id(self) -> None:
        entity = {"id": 1, "name": "Test"}
        self.repository.create(entity=entity)

        retrieved_entity = self.repository.retrieve_by_id(id=1)
        assert retrieved_entity.id == 1  # type: ignore
        assert retrieved_entity.name == "Test"  # type: ignore

    def test_retrieve(self) -> None:
        entity = {"id": 1, "name": "Test"}
        self.repository.create(entity=entity)

        retrieved_entity = self.repository.retrieve(name="Test")
        assert retrieved_entity.id == 1  # type: ignore
        assert retrieved_entity.name == "Test"  # type: ignore

    def test_update(self) -> None:
        entity = {"id": 1, "name": "Test"}
        self.repository.create(entity=entity)

        retrieved_entity = self.repository.update(id=1, entity={"id": 1, "name": "Test_Updated"})
        self.session.commit()

        with pytest.raises(ValueError):
            self.repository.update(id=1, entity={"id": 999, "name": "Test_Updated"})

        with pytest.raises(SQLAlchemyError):
            self.repository.retrieve(name="Test")

        retrieved_entity = self.repository.retrieve(name="Test_Updated")
        assert retrieved_entity.id == 1  # type: ignore
        assert retrieved_entity.name == "Test_Updated"  # type: ignore

        retrieved_entity = self.repository.update(id=1, entity={"name": "Test_Update_without_id"})
        self.session.commit()

        retrieved_entity = self.repository.retrieve(name="Test_Update_without_id")
        assert retrieved_entity.id == 1  # type: ignore
        assert retrieved_entity.name == "Test_Update_without_id"  # type: ignore

    def test_destroy_existing(self) -> None:
        entity = MockModel(id=4, name="Test")
        self.session.add(entity)
        self.session.commit()

        self.repository.destroy(id=4)

        destroyed_entity = self.session.query(MockModel).filter_by(id=4).first()
        assert destroyed_entity is None

    def test_list_with_filter_manager(self) -> None:
        filter_manager_mock = MagicMock()
        self.repository.get_base_query = MagicMock()  # type: ignore
        self.repository.list(filter_manager=filter_manager_mock, name="Test")
        filter_manager_mock.filter_queryset.assert_called()
        filter_manager_mock.order_by_queryset.assert_called()

    def test_list_with_pagination_manager(self) -> None:
        pagination_manager_mock = MagicMock()
        self.repository.get_base_query = MagicMock()  # type: ignore
        self.repository.list(pagination_manager=pagination_manager_mock, name="Test")
        pagination_manager_mock.paginate_queryset.assert_called()

    def test_perform_commit(self) -> None:
        session_mock = MagicMock()
        self.repository.session = session_mock
        self.repository.perform_commit()
        session_mock.commit.assert_called()

    def test_update_raises_value_error_on_mismatched_id(self) -> None:
        with pytest.raises(ValueError, match="ID in the entity does not match the given ID."):
            self.repository.update(id=1, entity={"id": 2})
