from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from collections import Counter
import logging
from typing import List, Dict, Any

from ..session_manager import get_session_data, SessionData
from .job_api_service import get_job_listings
from .ai_service import extract_skills_from_job_description

router = APIRouter()
logger = logging.getLogger(__name__)


# Pydantic models to match the new frontend's questionnaire data
class JourneyPayload(BaseModel):
    cv_skills: List[Dict[str, Any]]
    questionnaire_answers: Dict[str, Any]


@router.post("/submit-journey")
async def submit_journey(
        payload: JourneyPayload,
        session: SessionData = Depends(get_session_data)
):
    session.cv_skills = payload.cv_skills
    session.questionnaire_data = payload.questionnaire_answers

    # Extract roles for analysis from the questionnaire data
    answers = payload.questionnaire_answers
    selected_roles = answers.get('roles', [])
    # The new questionnaire uses a dynamic 'options' array, so 'roleOther' isn't a fixed key.
    # We will assume any non-predefined role is custom.
    # This part of the logic needs to be robust to handle the new questionnaire's data structure.

    target_roles = set(selected_roles)

    if not target_roles:
        raise HTTPException(status_code=400, detail="No target job roles provided.")

    all_market_skills = []
    for role in target_roles:
        job_descriptions = get_job_listings(job_title=role)
        for desc in job_descriptions:
            skills = extract_skills_from_job_description(desc)
            all_market_skills.extend(skills)

    skill_counts = Counter(all_market_skills)
    most_common_skills = [{"skill": item, "count": count} for item, count in skill_counts.most_common(20)]
    session.job_requirements = most_common_skills

    # The session_manager dependency automatically saves the updated session.
    return {"message": "Journey data processed and saved successfully."}