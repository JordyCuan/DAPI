import pytest
from pydantic_core import ValidationError

from utils.filters.schemas import FilterSchema


class TestFilterSchema:
    def test_extra_filter_lookups_forbid(self) -> None:
        valid_filters = {"field__gt": 10, "name__contains": "test"}

        with pytest.raises(ValidationError):
            FilterSchema(**valid_filters)

    def test_invalid_filter_lookups(self) -> None:
        class SampleFilterSchema(FilterSchema):
            field__invalid_lookup: int = 10

        invalid_filters = {"field__invalid_lookup": 11}
        with pytest.raises(
            ValueError, match=r"Filter attribute field__invalid_lookup should be a valid lookup:"
        ):
            SampleFilterSchema(**invalid_filters)
