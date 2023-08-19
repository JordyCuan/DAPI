from utils.services import BaseService


class TestBaseService:
    def test_get_by_id(self, mock_repository):
        service = BaseService(repository=mock_repository)
        result = service.get_by_id(id=1)
        mock_repository.retrieve_by_id.assert_called_once_with(id=1)
        assert result == mock_repository.retrieve_by_id.return_value

    def test_get(self, mock_repository):
        service = BaseService(repository=mock_repository)
        filters = {"key": "value"}
        result = service.get(**filters)
        mock_repository.retrieve.assert_called_once_with(**filters)
        assert result == mock_repository.retrieve.return_value

    def test_list(self, mock_repository):
        service = BaseService(repository=mock_repository)
        filters = {"key": "value"}
        result = service.list(**filters)
        mock_repository.list.assert_called_once_with(**filters)
        assert result == mock_repository.list.return_value

    def test_create(self, mock_repository):
        service = BaseService(repository=mock_repository)
        entity = {"key": "value"}
        result = service.create(entity=entity)
        mock_repository.create.assert_called_once_with(entity=entity)
        assert result == mock_repository.create.return_value

    def test_update(self, mock_repository):
        service = BaseService(repository=mock_repository)
        entity = {"key": "value"}
        result = service.update(id=1, entity=entity)
        mock_repository.update.assert_called_once_with(id=1, entity=entity)
        assert result == mock_repository.update.return_value

    def test_destroy(self, mock_repository):
        service = BaseService(repository=mock_repository)
        service.destroy(id=1)
        mock_repository.destroy.assert_called_once_with(id=1)
