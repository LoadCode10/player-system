from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title="The System API")
#print(f"Connecting to:{settings.DATABASE_URL}")

@app.get("/health")
def health():
    return {
        "status": "online",
        "message": "The System is awake."
    }