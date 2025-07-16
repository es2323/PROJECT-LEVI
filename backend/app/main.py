from fastapi import FastAPI
from .api.upload_cv import router as upload_cv_router
from .api.extract_skills import router as extract_skills_router
import uvicorn

app = FastAPI(title="CV Upload API", description="Simple API for CV text extraction and skill analysis")

app.include_router(upload_cv_router, prefix="/api")
app.include_router(extract_skills_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the CV Upload API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)