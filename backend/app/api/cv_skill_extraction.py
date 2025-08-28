from fastapi import APIRouter, UploadFile, File, HTTPException
import pdfplumber
import logging
import json
import os
import uuid
from dotenv import load_dotenv
# FIXED: Import the missing 'genai' library
import google.generativeai as genai

# Import from your custom modules
from ..session_manager import create_session_token, redis_client, SessionData, SESSION_TTL_SECONDS
from .ai_service import model

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/cv-skill-extraction")
async def cv_skill_extraction(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        new_session_id = str(uuid.uuid4())
        session_data = SessionData(session_id=new_session_id)

        with pdfplumber.open(file.file) as pdf:
            text = "".join(page.extract_text() for page in pdf.pages if page.extract_text())

        prompt = f"""
          Analyse the provided CV text to extract the candidate's skills.
          Your response must be a valid JSON object with a single key "skills".
          Example: {{"skills": [{{"name": "Python", "proficiency": 8, "confidence": 9}}]}}
          Do not include any other text or markdown formatting.
          CV Text: {text}
          """
        config = genai.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=config)
        extracted_data = json.loads(response.text)

        session_data.cv_skills = extracted_data.get("skills", [])

        await redis_client.set(
            f"session:{new_session_id}",
            session_data.model_dump_json(),
            ex=SESSION_TTL_SECONDS
        )

        session_token = create_session_token(new_session_id)
        return {"skills": session_data.cv_skills, "session_token": session_token}

    except Exception as e:
        logger.error(f"CV processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")