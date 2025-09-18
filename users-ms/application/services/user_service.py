from typing import List
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.use_cases.create_user import CreateUserUseCase
from domain.use_cases.get_all_users import GetAllUsersUseCase

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.create_user_use_case = CreateUserUseCase(user_repository)
        self.get_all_users_use_case = GetAllUsersUseCase(user_repository)

    def create_user(self, user: User) -> User:
        return self.create_user_use_case.execute(user)

    def get_all_users(self) -> List[User]:
        return self.get_all_users_use_case.execute()

