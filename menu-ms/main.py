from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

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