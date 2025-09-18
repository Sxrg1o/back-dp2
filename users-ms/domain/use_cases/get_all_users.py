from typing import List
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

class GetAllUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self) -> List[User]:
        return self.user_repository.get_all()

