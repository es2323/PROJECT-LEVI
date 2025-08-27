from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Tuple
from ..models import SubmissionPayload
from ..session import get_session, SessionData, backend

router = APIRouter()


@router.post("/submit-questionnaire")
async def submit_questionnaire(
    payload: SubmissionPayload, # <-- Use the Pydantic model for automatic validation
    session_info: Tuple[Any, SessionData] = Depends(get_session)
):
    """
    Receives validated CV skills and questionnaire data and saves it to the session.
    """
    session_id, session_data = session_info

    # The data from the frontend is now in `payload` and is guaranteed to be clean
    session_data.cv_skills = payload.cv_skills
    session_data.questionnaire_data = payload.questionnaire_answers

    # Update the session with the new data
    await backend.update(session_id, session_data)

    return {"message": "Questionnaire data saved successfully."}