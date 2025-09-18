from pydantic import BaseModel

class User(BaseModel):
    id: int | None = None  # ID autogenerado por la base de datos
    name: str
    email: str

    class Config:
        orm_mode = True
