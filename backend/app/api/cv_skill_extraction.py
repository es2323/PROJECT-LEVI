from fastapi import APIRouter, UploadFile, File, HTTPException
import pdfplumber
import logging
import os
import uuid
import dotenv
from dotenv import load_dotenv
from ..session_manager import create_session_token, redis_client, SessionData, SESSION_TTL_SECONDS
# Import the specific, renamed AI function
from .ai_service import extract_skills_from_cv

# Load .env and GENAI_API_KEY
dotenv.load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/cv-skill-extraction")
async def cv_skill_extraction(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        new_session_id = str(uuid.uuid4())
        print(f"DEBUG: Creating new session with ID: {new_session_id}")
        session_data = SessionData(session_id=new_session_id)

        with pdfplumber.open(file.file) as pdf:
            text = "".join(page.extract_text() for page in pdf.pages if page.extract_text())

        # Call the new, specific AI function for CVs
        extracted_skills = extract_skills_from_cv(text)
        session_data.cv_skills = extracted_skills

        await redis_client.set(
            f"session:{new_session_id}",
            session_data.model_dump_json(),
            ex=SESSION_TTL_SECONDS
        )

        session_token = create_session_token(new_session_id)

        # Return the extracted skills list and the token
        return {"skills": session_data.cv_skills, "session_token": session_token}

    except Exception as e:
        logger.error(f"CV processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")