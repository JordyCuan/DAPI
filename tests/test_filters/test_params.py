from unittest.mock import patch

from utils.filters.params import FilterParam


def test_filter_param_initialization() -> None:
    test_kwargs = {"description": "A test parameter", "alias": "test_param"}

    with patch("fastapi.params.Query.__init__") as mock_super_init:
        _ = FilterParam(**test_kwargs)

        mock_super_init.assert_called_once_with(None, **test_kwargs)
