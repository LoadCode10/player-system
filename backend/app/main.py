from fastapi import FastAPI

app = FastAPI(title="The System API")

@app.get("/health")
def health():
    return {
        "status": "online",
        "message": "The System is awake."
    }