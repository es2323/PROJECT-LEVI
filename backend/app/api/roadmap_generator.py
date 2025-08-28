from fastapi import APIRouter, Depends
import logging
import json

from ..session_manager import get_session_data, SessionData

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate-roadmap")
async def generate_roadmap(
    session: SessionData = Depends(get_session_data)
):
    """
    Gathers all previously collected data from the session and prints it
    to the console, confirming it's ready for the final LLM prompt.
    """
    logger.info(f"Gathering final data for roadmap for session: {session.session_id}")

    # Print all collected data to the backend console for verification.
    print("\n--- DEBUG: FINAL DATA COLLECTED FOR ROADMAP ---")
    print("CV Skills:", json.dumps(session.cv_skills, indent=2))
    print("Job Requirements:", json.dumps(session.job_requirements, indent=2))
    print("Questionnaire Answers:", json.dumps(session.questionnaire_data, indent=2))
    print("-------------------------------------------------\n")

    return { "message": "Data successfully gathered and ready for roadmap generation." }