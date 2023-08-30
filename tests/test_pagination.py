import json
from unittest.mock import MagicMock

import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from utils.pagination import LimitOffsetPagination, LimitOffsetSchema


class Base(DeclarativeBase):
    pass


class SampleModel(Base):
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True)
    name = Column(String)


@pytest.fixture
def sample_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()


class TestLimitOffsetSchema:
    def test_both_fields_set(self) -> None:
        schema = LimitOffsetSchema(limit=10, offset=5)
        assert schema.limit == 10
        assert schema.offset == 5

    def test_only_offset_set(self) -> None:
        with pytest.raises(ValueError):
            LimitOffsetSchema(offset=5)

    def test_only_limit_set(self) -> None:
        schema = LimitOffsetSchema(limit=10)
        assert schema.limit == 10


class TestLimitOffsetPagination:
    def test_pagination(self) -> None:
        mock_query = MagicMock()
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 10

        schema = LimitOffsetSchema(limit=4, offset=8)
        paginator = LimitOffsetPagination(schema=schema)

        _ = paginator.paginate_queryset(mock_query)

        mock_query.offset.assert_called_once_with(8)
        mock_query.limit.assert_called_once_with(4)
        mock_query.count.assert_called_once()

        assert paginator.count == 10

    def test_paginated_response(self) -> None:
        schema = LimitOffsetSchema(limit=5, offset=5)
        paginator = LimitOffsetPagination(schema=schema)
        paginator.count = 10
        response = paginator.get_paginated_response(data=[{"id": 1, "name": "test"}])
        assert response.status_code == 200

        body = json.loads(response.body)
        assert body["count"] == 10
        assert len(body["results"]) == 1
