import pytest

from utils.database.schemas import DatabaseProperties, DatabaseSettingsMixin


class TestDatabaseProperties:
    def test_database_properties_initialization(self):
        data = {
            "engine": "postgresql",
            "name": "testdb",
            "user": "testuser",
            "password": "testpass",
            "host": "localhost",
            "port": 5432,
        }
        db_props = DatabaseProperties(**data)
        for key, value in data.items():
            assert getattr(db_props, key) == value


class TestDatabaseSettingsMixin:
    def test_get_database_url(self):
        data = {
            "engine": "postgresql",
            "name": "testdb",
            "user": "testuser",
            "password": "testpass",
            "host": "localhost",
            "port": 5432,
        }
        expected_url = "postgresql://testuser:testpass@localhost:5432/testdb"

        mixin = DatabaseSettingsMixin(DATABASE=DatabaseProperties(**data))
        assert mixin.get_database_url() == expected_url
