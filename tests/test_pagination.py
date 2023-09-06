from unittest.mock import MagicMock

import pytest
from pydantic_core import ValidationError
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Query, sessionmaker

from utils.pagination import LimitOffsetPagination, LimitOffsetSchema, PageNumberPagination, PageNumberSchema


class Base(DeclarativeBase):
    pass


class SampleModel(Base):
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True)
    name = Column(String)


@pytest.fixture
def sample_query():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return session.query(SampleModel)


class TestPageNumberSchema:
    def test_both_fields_set(self) -> None:
        schema = PageNumberSchema(page_size=10, page=5)
        assert schema.page_size == 10
        assert schema.page == 5

    def test_both_fields_unset(self) -> None:
        schema = PageNumberSchema()
        assert schema.page_size is None
        assert schema.page is None

    def test_missing_one_field(self) -> None:
        with pytest.raises(ValidationError):
            PageNumberSchema(page=None, page_size=5)

        with pytest.raises(ValidationError):
            PageNumberSchema(page=5, page_size=None)


class TestLimitOffsetSchema:
    def test_both_fields_set(self) -> None:
        schema = LimitOffsetSchema(limit=10, offset=5)
        assert schema.limit == 10
        assert schema.offset == 5

    def test_both_fields_unset(self) -> None:
        schema = LimitOffsetSchema()
        assert schema.limit is None
        assert schema.offset is None

    def test_missing_one_field(self) -> None:
        with pytest.raises(ValidationError):
            LimitOffsetSchema(offset=None, limit=5)

        with pytest.raises(ValidationError):
            LimitOffsetSchema(offset=5, limit=None)


class TestPageNumberPagination:
    def test_paginated_response_data(self) -> None:
        schema = PageNumberSchema(page=2, page_size=2)
        paginator = PageNumberPagination(schema=schema)
        paginator.count = 6
        response_data = paginator.get_paginated_response_data(results=[{"id": 1, "name": "test"}])
        assert response_data["data"][0]["id"] == 1
        assert response_data["data"][0]["name"] == "test"

        assert response_data["pagination"]["count"] == 6
        assert response_data["pagination"]["page"] == 2
        assert response_data["pagination"]["page_size"] == 2
        assert response_data["pagination"]["previous_page"] == 1
        assert response_data["pagination"]["total_pages"] == 3
        assert response_data["pagination"]["next_page"] == 3

    def test_paginated_response_data_on_first_page(self) -> None:
        schema = PageNumberSchema(page=1, page_size=2)
        paginator = PageNumberPagination(schema=schema)
        paginator.count = 6
        response_data = paginator.get_paginated_response_data(results=[])
        assert "previous_page" not in response_data["pagination"]
        assert response_data["pagination"]["total_pages"] == 3
        assert response_data["pagination"]["next_page"] == 2

    def test_paginated_response_data_on_last_page(self) -> None:
        schema = PageNumberSchema(page=3, page_size=2)
        paginator = PageNumberPagination(schema=schema)
        paginator.count = 6
        response_data = paginator.get_paginated_response_data(results=[])
        assert response_data["pagination"]["previous_page"] == 2
        assert response_data["pagination"]["total_pages"] == 3
        assert "next_page" not in response_data["pagination"]

    def test_paginate_queryset(self, sample_query):
        schema = type("MockSchema", (), {"page": 2, "page_size": 10})
        paginator = PageNumberPagination(schema=schema)
        modified_query = paginator.paginate_queryset(sample_query)
        assert "LIMIT " in str(modified_query)
        assert "OFFSET " in str(modified_query)

    def test_get_pagination_properties(self):
        schema = type("MockSchema", (), {"page": 2, "page_size": 10})
        paginator = PageNumberPagination(schema=schema)
        paginator.count = 25
        props = paginator.get_pagination_properties()
        assert props["next_page"] == 3
        assert props["previous_page"] == 1

    def test_no_pagination_page_and_size(self):
        schema = type("MockSchema", (), {"page": None, "page_size": None})
        paginator = PageNumberPagination(schema=schema)
        paginator.count = 25
        props = paginator.get_pagination_properties()
        response_data = paginator.get_paginated_response_data(results=[])
        assert props == {}
        assert "pagination" not in response_data


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

    def test_paginated_response_data(self) -> None:
        schema = LimitOffsetSchema(limit=4, offset=8)
        paginator = LimitOffsetPagination(schema=schema)
        paginator.count = 10
        response_data = paginator.get_paginated_response_data(results=[{"id": 1, "name": "test"}])
        assert response_data["data"][0]["id"] == 1
        assert response_data["data"][0]["name"] == "test"

        assert response_data["pagination"]["count"] == 10
        assert response_data["pagination"]["limit"] == 4
        assert response_data["pagination"]["offset"] == 8

    def test_paginate_queryset(self, sample_query: Query[SampleModel]):
        schema = type("MockSchema", (), {"offset": 10, "limit": 10})
        paginator = LimitOffsetPagination(schema=schema)
        modified_query = paginator.paginate_queryset(sample_query)
        assert "LIMIT" in str(modified_query)
        assert "OFFSET" in str(modified_query)

    def test_get_pagination_properties(self):
        schema = type("MockSchema", (), {"offset": 10, "limit": 10})
        paginator = LimitOffsetPagination(schema=schema)
        paginator.count = 25
        props = paginator.get_pagination_properties()
        assert props["limit"] == 10
        assert props["offset"] == 10

    def test_no_pagination_limit_and_offset(self):
        schema = type("MockSchema", (), {"limit": None, "offset": None})
        paginator = LimitOffsetPagination(schema=schema)
        paginator.count = 25
        props = paginator.get_pagination_properties()
        response_data = paginator.get_paginated_response_data(results=[])
        assert props == {}
        assert "pagination" not in response_data
