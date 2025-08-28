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


# --- Pydantic Models ---
class RolesModel(BaseModel):
    predefined: List[str]
    genericOther: str
    customSectorRoles: Dict[str, str]

class QuestionnairePayload(BaseModel):
    sectors: List[str]
    roles: RolesModel
    ambition: str | None = None
    passion: List[str] = []
    confidence: str | None = None
    learningStyle: List[str] = []
    techPreference: str | None = None
    workPace: str | None = None

class AnalysisPayload(BaseModel):
    cv_skills: List[Dict[str, Any]]
    questionnaire_answers: QuestionnairePayload


@router.post("/analyse-market")
async def analyse_market(
    payload: AnalysisPayload,
    session: SessionData = Depends(get_session_data)
):
    """
    Receives questionnaire data, performs job market analysis, and saves
    all collected information to the user's session in Redis.
    """
    logger.info(f"Analysing market for session: {session.session_id}")

    # 1. Save the received CV skills and questionnaire data to the session.
    session.cv_skills = payload.cv_skills
    session.questionnaire_data = payload.questionnaire_answers.model_dump()

    # 2. Perform the job market analysis based on the roles.
    questionnaire = payload.questionnaire_answers
    target_roles = set(questionnaire.roles.predefined)
    if questionnaire.roles.genericOther:
        target_roles.add(questionnaire.roles.genericOther)
    target_roles.update(questionnaire.roles.customSectorRoles.values())

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

    return {"message": "Market analysis complete and data saved to session."}