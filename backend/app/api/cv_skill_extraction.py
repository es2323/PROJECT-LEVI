from fastapi import APIRouter, UploadFile, File, HTTPException
import pdfplumber
from pydantic import BaseModel
import google.generativeai as genai
import logging
import json

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Get API key from .env file
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.getenv("GENAI_API_KEY")
if not API_KEY:
    raise ValueError("GENAI_API_KEY not found in environment variables")

@router.post("/cv-skill-extraction")
async def cv_skill_extraction(file: UploadFile = File(...)):
    logger.info(f"Endpoint hit with file: {file.filename}")
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        # Extract text from PDF
        with pdfplumber.open(file.file) as pdf:
            text = ""
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
            if not text:
                raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")

        # Log the extracted text to the console
        logger.info(f"Extracted text: {text[:50]}...")  # Log first 50 characters

        # Configure Gemini API with the environment variable
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Simple prompt to extract skills
        prompt = f"""
          Extract a list of hard technical skills, such as "Python" from the provided CV text. Include only the candidate's name, skills, and proficiency levels, your proficiency assessment must be perfect, if you don't have enough information to make an accurate assessment return 0 for proficiency, emsure you're extremely harsh when deciding if you have enough information, as if you don't I'll collect more information from the user to get a more accurate picture.

          Format the response as a plain JSON string:
          {{"skills": [{{"name": "<skill_name>", "proficiency": "<proficiency_level>"}}, ...]}}

          Do not include any additional text, comments, or metadata in the response. Return ONLY valid JSON.

          CV Text: {text}
          """

        # Generate content with Gemini
        response = model.generate_content(prompt)
        logger.info(f"Raw Gemini response: {response.text}")

        # Remove backticks and "json" from the response
        json_string = response.text.replace("```json", "").replace("```", "")

        # Parse the JSON string into a Python object
        try:
            extracted_skills = json.loads(json_string)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            raise HTTPException(status_code=500, detail="Failed to decode JSON from Gemini response")

        return {"extracted_skills": extracted_skills}

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))