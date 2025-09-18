from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.db import SessionLocal
from domain.entities.user import User
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from application.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepositoryImpl(db)
    return UserService(repository)

@router.get("/", response_model=list[User])
def list_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.post("/", response_model=User)
def create_user(user: User, service: UserService = Depends(get_user_service)):
    return service.create_user(user)
