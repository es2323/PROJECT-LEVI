from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from collections import Counter
import logging
import json
from typing import List, Dict, Any

from ..session_manager import get_session_data, SessionData
from .job_api_service import get_job_listings
from .ai_service import extract_skills_from_job_description, synthesize_skills

router = APIRouter()
logger = logging.getLogger(__name__)

# This dictionary translates frontend role IDs into better search terms for the Adzuna API.
# You should expand this map for all your roles.
ROLE_TO_SEARCH_TERM_MAP = {
    "mobile_ridesharing": "Mobile App Developer Ridesharing",
    "backend_fleet": "Backend Fleet Management Engineer",
    "computer_vision_adas": "Computer Vision Engineer ADAS",
    "quant_dev": "Quantitative Developer",
    "backend_payments": "Backend Payments Engineer",
    "cybersec_finance": "Cybersecurity Finance",
    "swe": "Software Engineer"
}


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
    answers = payload.questionnaire_answers

    target_roles = set(answers.get('roles', []))
    if answers.get('roleOther'):
        target_roles.add(answers.get('roleOther'))

    if not target_roles:
        raise HTTPException(status_code=400, detail="No target job roles provided.")

    raw_skills_by_role = {}
    for role in target_roles:
        # Use the map to get a better search term, falling back to the role ID itself
        search_term = ROLE_TO_SEARCH_TERM_MAP.get(role, role)
        logger.info(f"Searching for job ads with term: '{search_term}'")

        job_descriptions = get_job_listings(job_title=search_term)
        current_role_skills = []
        for desc in job_descriptions:
            skills = extract_skills_from_job_description(desc)
            current_role_skills.extend(skills)
        # Store the collected skills under the original role name for consistency
        raw_skills_by_role[role] = list(set(current_role_skills))

    if raw_skills_by_role:
        synthesized_job_requirements = synthesize_skills(raw_skills_by_role)
    else:
        synthesized_job_requirements = {"skills_by_role": {}, "common_skills": []}

    session.job_requirements = synthesized_job_requirements

    # --- Skill Comparison Logic ---
    user_skill_set = {skill['name'].lower().strip() for skill in session.cv_skills if skill.get('name')}
    missing_skills_by_role = {}
    for role, required_skills in synthesized_job_requirements.get("skills_by_role", {}).items():
        required_skill_set = {skill.lower().strip() for skill in required_skills}
        missing = list(required_skill_set - user_skill_set)
        missing_skills_by_role[role] = missing

    common_required_set = {skill.lower().strip() for skill in synthesized_job_requirements.get("common_skills", [])}
    missing_common_skills = list(common_required_set - user_skill_set)

    missing_skills_result = {
        "skills_by_role": missing_skills_by_role,
        "common_skills": missing_common_skills
    }
    session.missing_skills = missing_skills_result

    print("DEBUG: Final session data state:")
    print(json.dumps(session.model_dump(), indent=2))

    return {"message": "Job analysis and skill comparison complete."}