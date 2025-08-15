from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import pdfplumber
import google.generativeai as genai
import logging
import json
import os
from dotenv import load_dotenv
from typing import Tuple, Any

# Adjust import path to point to the new session file
from ..session import get_session, SessionData, backend

# Load environment variables
load_dotenv()
router = APIRouter()
logger = logging.getLogger(__name__)

# Configure Gemini model
GEMINI_API_KEY = os.getenv("GENAI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GENAI_API_KEY not found in .env file.")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

@router.post("/cv-skill-extraction")
async def cv_skill_extraction(
    file: UploadFile = File(...),
    session_info: Tuple[Any, SessionData] = Depends(get_session)
):
    """
    Extracts skills from a CV, saves them to the user's session, and returns them.
    """
    session_id, session_data = session_info
    logger.info(f"Processing CV for session_id: {session_id}")
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        with pdfplumber.open(file.file) as pdf:
            text = "".join(page.extract_text() for page in pdf.pages if page.extract_text())
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

        prompt = f"""
          Analyse the provided CV text to extract the candidate's skills.
          Your response MUST be a JSON object with a single key "skills".
          This key should hold a list of objects, where each object has three keys: "name", "proficiency", and "confidence".
          Example: {{"skills": [{{"name": "Python", "proficiency": 8, "confidence": 9}}]}}
          Do not include any other text or markdown formatting.

          CV Text: {text}
          """
        config = genai.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=config)
        extracted_data = json.loads(response.text)

        # Update the session with the new skill data
        session_data.cv_skills = extracted_data.get("skills", [])
        await backend.update(session_id, session_data)

        logger.info(f"Successfully extracted and stored skills for session_id: {session_id}")
        return extracted_data

    except Exception as e:
        logger.error(f"Error processing CV for session_id: {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
