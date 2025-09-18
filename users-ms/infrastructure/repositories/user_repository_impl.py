from sqlalchemy.orm import Session
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.models.user_model import UserModel

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[User]:
        db_users = self.db.query(UserModel).all()
        return [User(id=db_user.id, name=db_user.name, email=db_user.email) for db_user in db_users]

    def create(self, user: User) -> User:
        db_user = UserModel(name=user.name, email=user.email)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return User(id=db_user.id, name=db_user.name, email=db_user.email)

