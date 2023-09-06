from typing import Optional

import pytest
from fastapi import Query
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from utils.filters.core import BaseFilterManager
from utils.filters.schemas import FilterSchema


class Base(DeclarativeBase):
    pass


class SampleModel(Base):
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class SampleFilterSchema(FilterSchema):
    name__icontains: Optional[str] = Query(None)


@pytest.fixture
def sample_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()


class TestBaseFilterManager:
    def test_filter_queryset(self, sample_session: Session) -> None:
        filter_schema = SampleFilterSchema(**{"name__icontains": "test"})

        filter_manager = BaseFilterManager(filters=filter_schema)
        filter_manager.model = SampleModel

        query = sample_session.query(SampleModel)
        filtered_query = filter_manager.filter_queryset(query)  # type: ignore[arg-type]

        # Asserting that the filter conditions were added to the query
        assert "ILIKE" in str(filtered_query) or "LIKE lower(" in str(filtered_query)

        # Asserting the query is the same when filters is empty
        filter_manager.filters = {}
        query = sample_session.query(SampleModel)
        filter_is_empty_query = filter_manager.filter_queryset(query)  # type: ignore[arg-type]
        assert filter_is_empty_query == query

    def test_order_by_queryset(self, sample_session: Session) -> None:
        filter_manager = BaseFilterManager(filters=FilterSchema(), ordering=["-name", "+age", "id"])
        filter_manager.model = SampleModel

        query = sample_session.query(SampleModel)
        ordered_query = filter_manager.order_by_queryset(query)  # type: ignore[arg-type]
        assert "ORDER BY" in str(ordered_query)

        # No ordering case
        query = sample_session.query(SampleModel)
        filter_manager.ordering = None
        query_without_ordering = filter_manager.order_by_queryset(query)  # type: ignore[arg-type]
        assert query_without_ordering == query
