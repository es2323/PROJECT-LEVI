from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Tuple

# Import the session management tools
from ..session import get_session, SessionData, backend

router = APIRouter()


@router.post("/submit-questionnaire")
async def submit_questionnaire(
        questionnaire_data: Dict[str, Any],
        session_info: Tuple[Any, SessionData] = Depends(get_session)
):
    """
    Receives questionnaire data from the frontend and saves it to the current session.
    """
    session_id, session_data = session_info

    # Update the session with the questionnaire data
    session_data.questionnaire_data = questionnaire_data
    await backend.update(session_id, session_data)

    return {"message": "Questionnaire data saved successfully."}
