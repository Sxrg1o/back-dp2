from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.db import SessionLocal
from domain.entities.user import User
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[User])
def list_users(db: Session = Depends(get_db)):
    repo = UserRepositoryImpl(db)
    return repo.get_all()

@router.post("/", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    repo = UserRepositoryImpl(db)
    return repo.create(user)
