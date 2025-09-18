from sqlalchemy import Column, Integer, String
from infrastructure.db import Base
from pydantic import BaseModel

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)


class CreateUserRequest(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
