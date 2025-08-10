from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import cv_skill_extraction, job_analyser

app = FastAPI(title="Project Levi API")

# --- CORS Middleware ---
origins = [
    "http://localhost:5173",  # The default origin for a Vue.js frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include All Routers ---
app.include_router(cv_skill_extraction.router, prefix="/api")
app.include_router(job_analyser.router, prefix="/api")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Project Levi API!"}