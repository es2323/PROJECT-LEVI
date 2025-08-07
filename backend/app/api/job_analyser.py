from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from collections import Counter
import logging
from typing import List, Dict
from .job_api_service import get_job_listings
from .ai_service import extract_skills_from_job_description

router = APIRouter()
logger = logging.getLogger(__name__)

class RolesModel(BaseModel):
    predefined: List[str] = []
    genericOther: str = ""
    customSectorRoles: Dict[str, str] = {}

class MarketAnalysisRequest(BaseModel):
    sectors: List[str]
    roles: RolesModel

@router.post("/analyse-market")
async def analyse_market_for_job(data: MarketAnalysisRequest):
    logger.info("Received request to analyse job market.")
    target_roles = set(data.roles.predefined)
    if data.roles.genericOther:
        target_roles.add(data.roles.genericOther)
    target_roles.update(data.roles.customSectorRoles.values())

    if not target_roles:
        raise HTTPException(status_code=400, detail="No target job roles provided.")

    logger.info(f"Consolidated target roles: {list(target_roles)}")
    all_market_skills = []
    for role in target_roles:
        logger.info(f"Analysing role: {role}")
        job_descriptions = get_job_listings(job_title=role)
        for desc in job_descriptions:
            skills = extract_skills_from_job_description(desc)
            all_market_skills.extend(skills)

    if not all_market_skills:
        return {"message": "Analysis complete, but no specific skills were extracted.", "market_skills": []}

    skill_counts = Counter(all_market_skills)
    most_common_skills = [{"skill": item, "count": count} for item, count in skill_counts.most_common(20)]
    logger.info(f"Analysis complete. Found {len(most_common_skills)} common skills.")
    return {"market_skills": most_common_skills}