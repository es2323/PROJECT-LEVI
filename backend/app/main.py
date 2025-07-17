from fastapi import FastAPI
from .api.upload_cv import router as upload_cv_router
from .api.extract_skills import router as extract_skills_router
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
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

app.include_router(upload_cv_router, prefix="/api")
app.include_router(extract_skills_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the CV Upload API!"}
