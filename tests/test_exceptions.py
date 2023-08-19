import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from utils.exceptions import HTTPBaseException


class TestSuperCall(unittest.TestCase):
    def test_super_init_called(self):
        with patch.object(HTTPException, "__init__", MagicMock()) as mock_super_init:
            HTTPBaseException.status_code = 500
            HTTPBaseException.detail = "Test"
            exc = HTTPBaseException()
            mock_super_init.assert_called_once()
