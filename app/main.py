from fastapi import FastAPI
from .database import engine
from .models import Base

app = FastAPI(title="Employee Management API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}
