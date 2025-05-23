from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import items
from app.core.database import engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRUD API",
    description="A CRUD API with FastAPI and SQLAlchemy",
    version="1.0.0"
)

# Configure CORS to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the CRUD API"}