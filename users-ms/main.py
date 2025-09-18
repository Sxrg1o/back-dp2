from fastapi import FastAPI
import uvicorn
import os

from infrastructure.db import Base, engine
from infrastructure.models.user_model import UserModel
from infrastructure.handlers.user_handler import router as user_router

# Configurar FastAPI para trabajar detrás de un proxy
app = FastAPI(
    title="Users Microservice",
    description="API for user management and authentication",
    version="1.0.0",
    root_path="/api/users",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

# Crear tablas
Base.metadata.create_all(bind=engine)

app.include_router(user_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))  # default 8002
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )