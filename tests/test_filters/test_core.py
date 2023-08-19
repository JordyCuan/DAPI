from typing import Optional

import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.filters import FilterParam
from utils.filters.core import BaseFilterManager
from utils.filters.schemas import FilterSchema

Base = declarative_base()


class SampleModel(Base):  # type: ignore[valid-type, misc]
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class SampleFilterSchema(FilterSchema):
    name__icontains: Optional[str] = FilterParam()


@pytest.fixture
def sample_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


class TestBaseFilterManager:
    def test_filter_queryset(self, sample_session):
        filter_schema = SampleFilterSchema(**{"name__icontains": "test"})

        filter_manager = BaseFilterManager(filters=filter_schema)
        filter_manager.model = SampleModel

        query = sample_session.query(SampleModel)
        filtered_query = filter_manager.filter_queryset(query)

        # Asserting that the filter conditions were added to the query
        assert "ILIKE" in str(filtered_query) or "LIKE lower(" in str(filtered_query)

    def test_order_by_queryset(self, sample_session):
        filter_manager = BaseFilterManager(filters=FilterSchema())
        filter_manager.model = SampleModel
        filter_manager.ordering = ["-name"]

        query = sample_session.query(SampleModel)
        ordered_query = filter_manager.order_by_queryset(query)

        # Asserting that the order_by condition was added to the query
        assert "ORDER BY" in str(ordered_query)

    def test_paginate_queryset(self, sample_session):
        filter_manager = BaseFilterManager(filters=FilterSchema())
        query = sample_session.query(SampleModel)
        paginated_query = filter_manager.paginate_queryset(query)

        assert paginated_query == query
