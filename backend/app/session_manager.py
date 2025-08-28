import uuid
import os
from typing import List, Dict, Any
import logging

import redis.asyncio as redis
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
SESSION_TTL_SECONDS = 3600  # 1 hour
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "a_very_secret_and_long_key_for_hs256")
ALGORITHM = "HS256"

redis_client = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
bearer_scheme = HTTPBearer()
logger = logging.getLogger(__name__)


# --- JWT Helper Functions ---
def create_session_token(session_id: str) -> str:
    """Creates a JWT containing the session ID."""
    to_encode = {"sub": session_id}
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)


def decode_session_token(token: str) -> str | None:
    """Decodes a JWT and returns the session ID."""
    try:
        if not token or not isinstance(token, str):
            return None
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError as e:
        logger.error(f"Token validation failed: {e}")
        return None


# --- Session Data Model ---
class SessionData(BaseModel):
    session_id: str
    cv_skills: List[Dict[str, Any]] = Field(default_factory=list)
    job_requirements: List[Dict[str, Any]] = Field(default_factory=list)
    questionnaire_data: Dict[str, Any] = Field(default_factory=dict)


# --- CORRECTED Session Management Dependency ---
async def get_session_data(
        auth: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> SessionData:
    """
    This dependency now uses a try/yield/finally block to ensure that
    any modifications to the session object are saved back to Redis
    after the endpoint has finished executing.
    """
    if not auth:
        raise HTTPException(status_code=401, detail="No authorization token provided")

    session_id = decode_session_token(auth.credentials)
    if not session_id:
        raise HTTPException(status_code=401, detail="Invalid or expired session token")

    raw_data = await redis_client.get(f"session:{session_id}")
    if not raw_data:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    session_data_obj = SessionData.model_validate_json(raw_data)

    try:
        # 1. Provide the loaded session data to the endpoint.
        yield session_data_obj
    finally:
        # 2. After the endpoint is finished, this code runs.
        # It saves the (potentially modified) session data back to Redis.
        json_data = session_data_obj.model_dump_json()
        await redis_client.set(
            f"session:{session_data_obj.session_id}",
            json_data,
            ex=SESSION_TTL_SECONDS
        )
        print(f"DEBUG: Session data saved for session_id: {session_data_obj.session_id}")