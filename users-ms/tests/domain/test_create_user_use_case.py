import pytest
from unittest.mock import Mock
from domain.entities.user import User
from domain.use_cases.create_user import CreateUserUseCase

class TestCreateUserUseCase:
    def test_execute_creates_user_successfully(self):
        # Arrange
        mock_repository = Mock()
        expected_user = User(id=1, name="John Doe", email="john@example.com")
        mock_repository.create.return_value = expected_user

        use_case = CreateUserUseCase(mock_repository)
        input_user = User(name="John Doe", email="john@example.com")

        # Act
        result = use_case.execute(input_user)

        # Assert
        mock_repository.create.assert_called_once_with(input_user)
        assert result == expected_user
        assert result.id == 1
        assert result.name == "John Doe"
        assert result.email == "john@example.com"

