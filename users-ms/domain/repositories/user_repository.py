from abc import ABC, abstractmethod
from domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass
