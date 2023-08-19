from unittest.mock import MagicMock, Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.database.models import APIBaseModel

DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="module")
def engine():
    return create_engine(DATABASE_URL)


@pytest.fixture(scope="module")
def create_tables(engine):
    APIBaseModel.metadata.create_all(bind=engine)
    yield
    APIBaseModel.metadata.drop_all(bind=engine)


@pytest.fixture
def session(engine, create_tables):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def mock_repository():
    mock = Mock()
    mock.retrieve_by_id.return_value = MagicMock()
    mock.retrieve.return_value = MagicMock()
    mock.list.return_value = [MagicMock()]
    mock.create.return_value = MagicMock()
    mock.update.return_value = MagicMock()
    return mock
