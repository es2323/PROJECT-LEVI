from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Tuple, Any

# Import from your session and api files
from .session import get_session, SessionData
from .api import cv_skill_extraction, journey # Import the new journey router

app = FastAPI(title="Project Levi API")

# --- Middleware ---
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(cv_skill_extraction.router, prefix="/api")
app.include_router(journey.router, prefix="/api") # Use the new journey router

# --- Endpoints ---

@app.get("/")
async def read_root():
    """Root endpoint for API health check."""
    return {"message": "Welcome to the Project Levi API!"}


@app.get("/api/session-data", response_model=SessionData)
async def get_current_session_data(
    session_info: Tuple[Any, SessionData] = Depends(get_session)
):
    """Debug endpoint to view the data in the current session."""
    _, session_data = session_info
    return session_data
