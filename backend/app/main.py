from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.db.session import get_db

app = FastAPI(title="The System API")
#print(f"Connecting to:{settings.DATABASE_URL}")

@app.get("/health")
def health():
    return {
        "status": "online",
        "message": "The System is awake."
    }

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {
        "status" : "online",
        "result" : result
    }