from fastapi import FastAPI
from .database import engine
from .models import Base
from .routes import router

app = FastAPI(title="Employee Management API")

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def health():
    return {"status": "ok"}