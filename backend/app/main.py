from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import cv_skill_extraction, roadmap_generator, job_analyser

app = FastAPI(title="Project Levi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv_skill_extraction.router, prefix="/api")
app.include_router(job_analyser.router, prefix="/api")
app.include_router(roadmap_generator.router, prefix="/api")

# ... (rest of your main.py file)