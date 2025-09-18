import pytest
from unittest.mock import Mock
from domain.entities.user import User
from application.services.user_service import UserService

class TestUserService:
    def test_create_user_delegates_to_use_case(self):
        # Arrange
        mock_repository = Mock()
        expected_user = User(id=1, name="Jane Doe", email="jane@example.com")
        mock_repository.create.return_value = expected_user

        service = UserService(mock_repository)
        input_user = User(name="Jane Doe", email="jane@example.com")

        # Act
        result = service.create_user(input_user)

        # Assert
        assert result == expected_user
        mock_repository.create.assert_called_once_with(input_user)

    def test_get_all_users_delegates_to_use_case(self):
        # Arrange
        mock_repository = Mock()
        expected_users = [
            User(id=1, name="John", email="john@example.com"),
            User(id=2, name="Jane", email="jane@example.com")
        ]
        mock_repository.get_all.return_value = expected_users

        service = UserService(mock_repository)

        # Act
        result = service.get_all_users()

        # Assert
        assert result == expected_users
        mock_repository.get_all.assert_called_once()

