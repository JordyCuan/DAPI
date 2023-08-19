from unittest.mock import patch

from utils.filters.param_functions import FilterParam


def test_filter_param():
    test_kwargs = {"description": "Test", "deprecated": False, "include_in_schema": True}

    with patch("utils.filters.params.FilterParam") as mock_function:
        mock_function.side_effect = lambda **kwargs: kwargs
        result = FilterParam(**test_kwargs)
        mock_function.assert_called_once_with(**test_kwargs)

        assert result == test_kwargs
