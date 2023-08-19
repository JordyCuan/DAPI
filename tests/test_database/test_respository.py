from unittest.mock import MagicMock

import pytest
from sqlalchemy import Column, String
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.database.models import APIBaseModel
from utils.database.repository import BaseRepository
from utils.exceptions import ImproperlyConfigured


class MockModel(APIBaseModel):
    name = Column(String)


class TestBaseRepository:
    @pytest.fixture(autouse=True)
    def setup_class(self, session):
        self.session = session
        self.repository = BaseRepository(session=session)
        self.repository.model = MockModel

    def test_get_model(self):
        assert self.repository.get_model() == MockModel

        self.repository.model = None
        with pytest.raises(ImproperlyConfigured):
            self.repository.get_model()

    def test_create(self):
        entity = {"id": 1, "name": "Test"}
        self.repository.create(entity=entity)

        created_entity = self.session.query(MockModel).first()
        assert created_entity.id == 1
        assert created_entity.name == "Test"

        with pytest.raises(IntegrityError):
            self.repository.create(entity=entity)

    def test_retrieve_by_id(self):
        entity = {"id": 1, "name": "Test"}
        self.repository.create(entity=entity)

        retrieved_entity = self.repository.retrieve_by_id(id=1)
        assert retrieved_entity.id == 1
        assert retrieved_entity.name == "Test"

    def test_retrieve(self):
        entity = {"id": 1, "name": "Test"}
        self.repository.create(entity=entity)

        retrieved_entity = self.repository.retrieve(name="Test")
        assert retrieved_entity.id == 1
        assert retrieved_entity.name == "Test"

    def test_update(self):
        entity = {"id": 1, "name": "Test"}
        self.repository.create(entity=entity)

        retrieved_entity = self.repository.update(id=1, entity={"id": 1, "name": "Test_Updated"})
        self.session.commit()

        with pytest.raises(ValueError):
            self.repository.update(id=1, entity={"id": 999, "name": "Test_Updated"})

        with pytest.raises(SQLAlchemyError):
            self.repository.retrieve(name="Test")

        retrieved_entity = self.repository.retrieve(name="Test_Updated")
        assert retrieved_entity.id == 1
        assert retrieved_entity.name == "Test_Updated"

        retrieved_entity = self.repository.update(id=1, entity={"name": "Test_Update_without_id"})
        self.session.commit()

        retrieved_entity = self.repository.retrieve(name="Test_Update_without_id")
        assert retrieved_entity.id == 1
        assert retrieved_entity.name == "Test_Update_without_id"

    def test_destroy_existing(self):
        entity = MockModel(id=4, name="Test")
        self.session.add(entity)
        self.session.commit()

        self.repository.destroy(id=4)

        destroyed_entity = self.session.query(MockModel).filter_by(id=4).first()
        assert destroyed_entity is None

    def test_list_with_filter_manager(self):
        filter_manager_mock = MagicMock()
        self.repository.get_base_query = MagicMock()
        self.repository.set_filter_manager(filter_manager_mock)
        self.repository.list(name="Test")
        filter_manager_mock.filter_queryset.assert_called()
        filter_manager_mock.order_by_queryset.assert_called()

    def test_perform_commit(self):
        session_mock = MagicMock()
        self.repository.session = session_mock
        self.repository.perform_commit()
        session_mock.commit.assert_called()

    def test_filter_queryset(self):
        query_mock = MagicMock()
        result = self.repository.filter_queryset(query_mock)
        assert result == query_mock

    def test_order_by_queryset(self):
        query_mock = MagicMock()
        result = self.repository.order_by_queryset(query_mock)
        assert result == query_mock

    def test_paginate_queryset(self):
        query_mock = MagicMock()
        result = self.repository.paginate_queryset(query_mock)
        assert result == query_mock

    def test_update_raises_value_error_on_mismatched_id(self):
        with pytest.raises(ValueError, match="ID in the entity does not match the given ID."):
            self.repository.update(id=1, entity={"id": 2})

    def test_update_on_non_existing_entry(self):
        self.repository.get_base_query = MagicMock()
        query_mock = MagicMock()
        query_mock.filter_by.return_value = query_mock
        query_mock.count.return_value = 0
        self.repository.get_base_query.return_value = query_mock

        with pytest.raises(AssertionError, match="Update on non existing entry or multiple entries found"):
            self.repository.update(id=1, entity={"id": 1})
