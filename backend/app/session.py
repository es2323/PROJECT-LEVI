import uuid
import os
from typing import List, Dict, Any, Tuple

from fastapi import Depends, Response, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier

# Load environment variables from .env file
load_dotenv()

# Get the secret key from the environment variables
SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "REPLACE_THIS_WITH_A_STRONG_SECRET_KEY")

# --- 1. Session Data Model ---

class SessionData(BaseModel):
    """Pydantic model defining the data stored in a user's session."""
    cv_skills: List[Dict[str, Any]] = Field(default_factory=list)
    job_requirements: List[Dict[str, Any]] = Field(default_factory=list)
    questionnaire_data: Dict[str, Any] = Field(default_factory=dict)

# --- 2. Backend and Verifier Configuration ---

# Use the InMemoryBackend for now. This can be swapped for RedisBackend later.
backend = InMemoryBackend[uuid.UUID, SessionData]()

class BasicVerifier(SessionVerifier[uuid.UUID, SessionData]):
    """Verifies the session is valid."""
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[uuid.UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """For anonymous sessions, we just need to confirm it exists."""
        return True

# Initialize the verifier
verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=False,
    backend=backend,
    auth_http_exception=HTTPException(403, "Not authenticated"),
)

# Initialize the session cookie
cookie = SessionCookie(
    cookie_name="session_id",
    identifier="general_verifier",
    auto_error=False,
    secret_key=SECRET_KEY,
    cookie_params=CookieParameters(),
)

# --- 3. Session Dependency ---

async def get_session(
    response: Response,
    session_id: uuid.UUID = Depends(cookie),
) -> Tuple[uuid.UUID, SessionData]:
    """
    Dependency to manage session creation and retrieval.
    Returns a tuple of (session_id, session_data).
    """
    if not session_id:
        session_data = SessionData()
        new_session_id = uuid.uuid4()
        await backend.create(new_session_id, session_data)
        # Use the correct method to attach the cookie to the response
        cookie.attach_to_response(response, new_session_id)
        return new_session_id, session_data

    session_data = await backend.read(session_id)
    if not session_data:
        session_data = SessionData()
        new_session_id = uuid.uuid4()
        await backend.create(new_session_id, session_data)
        # Use the correct method to attach the cookie to the response
        cookie.attach_to_response(response, new_session_id)
        return new_session_id, session_data

    return session_id, session_data