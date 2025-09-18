from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user: User) -> User:
        # Aquí podría ir validación de negocio
        # Por ejemplo: verificar que el email no exista, validar formato, etc.
        return self.user_repository.create(user)

