from fastapi import FastAPI
from .api.cv_skill_extraction import router as cv_skill_extraction_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CV Upload API", description="Simple API for CV text extraction and skill analysis")

origins = [
    "http://localhost:5173",  # The origin of your Vue.js frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv_skill_extraction_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the CV Upload API!"}
