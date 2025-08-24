from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from collections import Counter
import logging
from typing import List, Dict, Tuple, Any
from ..models import FinalPayload

# Import shared components
from ..session import get_session, SessionData, backend
from .job_api_service import get_job_listings
from .ai_service import extract_skills_from_job_description

router = APIRouter()
logger = logging.getLogger(__name__)


# Define the Pydantic models for the incoming data
class RolesModel(BaseModel):
    predefined: List[str] = []
    genericOther: str = ""
    customSectorRoles: Dict[str, str] = {}


class JourneyPayload(BaseModel):
    sectors: List[str]
    roles: RolesModel
    ambition: str | None = None
    passion: List[str] = []
    confidence: str | None = None
    learningStyle: List[str] = []
    techPreference: str | None = None
    workPace: str | None = None


@router.post("/submit-journey")
async def submit_journey_data(
    payload: FinalPayload,
    session_info: Tuple[Any, SessionData] = Depends(get_session)
):
    session_id, session_data = session_info

    # Save the CV skills and validated questionnaire answers to the session
    session_data.cv_skills = payload.cv_skills
    session_data.questionnaire_data = payload.questionnaire_answers

    await backend.update(session_id, session_data)

    # ... (The market analysis logic can now be triggered here) ...

    return {"message": "Complete journey data saved successfully."}

