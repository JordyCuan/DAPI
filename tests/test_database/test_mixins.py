import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

from utils.database.mixins import TimestampMixin
from utils.database.models import APIBaseModel


class SampleModel(APIBaseModel, TimestampMixin):
    name = Column(String)


class TestTimestampMixin:
    def test_default_timestamps(self, session):
        instance = SampleModel(name="Test")
        session.add(instance)
        session.commit()
        assert instance.created_at is not None
        assert instance.updated_at is not None

    def test_updated_at_changes(self, session):
        instance = SampleModel(name="Original")
        session.add(instance)
        session.commit()

        original_updated_at = instance.updated_at
        instance.name = "Updated"
        session.commit()
        assert instance.updated_at != original_updated_at
