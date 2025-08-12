from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from collections import Counter
import logging
from typing import List, Dict, Tuple, Any

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
        payload: JourneyPayload,
        session_info: Tuple[Any, SessionData] = Depends(get_session)
):
    """
    A single endpoint to process job roles and questionnaire answers.
    """
    session_id, session_data = session_info
    logger.info(f"Processing full journey data for session_id: {session_id}")

    # --- 1. Perform Job Market Analysis ---
    target_roles = set(payload.roles.predefined)
    if payload.roles.genericOther:
        target_roles.add(payload.roles.genericOther)
    target_roles.update(payload.roles.customSectorRoles.values())

    if target_roles:
        all_market_skills = []
        for role in target_roles:
            job_descriptions = get_job_listings(job_title=role)
            for desc in job_descriptions:
                skills = extract_skills_from_job_description(desc)
                all_market_skills.extend(skills)

        skill_counts = Counter(all_market_skills)
        most_common_skills = [{"skill": item, "count": count} for item, count in skill_counts.most_common(20)]
        session_data.job_requirements = most_common_skills
        logger.info(f"Saved {len(most_common_skills)} job requirements for session {session_id}")

    # --- 2. Save Questionnaire Data ---
    session_data.questionnaire_data = payload.dict()
    logger.info(f"Saved questionnaire data for session {session_id}")

    # --- 3. Update the session in one go ---
    await backend.update(session_id, session_data)

    return {"message": "Journey data saved successfully."}

