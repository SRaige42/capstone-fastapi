from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import auth, student, instructor, admin
from .config import settings

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://brave.com",
    "https://google.com",
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(instructor.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": f"Welcome to the FastAPI application for the education management system! Using database: {settings.DATABASE_URL}"}
