from fastapi import APIRouter, UploadFile, File, HTTPException
import pdfplumber
import google.generativeai as genai
import logging
import json
import os

router = APIRouter()
logger = logging.getLogger(__name__)

# This router uses the Gemini model configured in ai_service.py
# Re-using the same configuration is more efficient
GEMINI_API_KEY = os.getenv("GENAI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GENAI_API_KEY not found in .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest') # Corrected model name

@router.post("/cv-skill-extraction")
async def cv_skill_extraction(file: UploadFile = File(...)):
    logger.info(f"Processing CV file: {file.filename}")
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
          This key should hold a list of objects, where each object has three keys: "name" (the skill), "proficiency" (your assessment on a scale of 1-10), and "confidence" (your confidence in the assessment, 1-10).
          Example: {{"skills": [{{"name": "Python", "proficiency": 8, "confidence": 9}}]}}
          Do not include any other text or markdown formatting.

          CV Text: {text}
          """
        config = genai.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=config)

        logger.info("Successfully extracted skills from CV.")
        return json.loads(response.text)

    except Exception as e:
        logger.error(f"Error processing CV: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))