from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the two primary routers for the new workflow
from .api import cv_skill_extraction, journey

app = FastAPI(title="Project Levi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv_skill_extraction.router, prefix="/api")
app.include_router(journey.router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Project Levi API is operational."}