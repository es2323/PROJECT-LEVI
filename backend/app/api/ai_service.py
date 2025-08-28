import json
import google.generativeai as genai
import logging
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GENAI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GENAI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')
logger = logging.getLogger(__name__)

def extract_skills_from_job_description(job_description: str) -> list[str]:
    """Uses the Gemini API to extract a list of skills from a job description."""
    if not job_description:
        return []
    prompt = (
        "Extract key skills, tools, and technologies from the job description. "
        "Return the output ONLY as a JSON object with a single key 'skills', containing a list of strings. "
        "Example: {\"skills\": [\"Python\", \"React\", \"SQL\"]}. "
        "If no skills are found, return {\"skills\": []}.\n\nJob Description:\n"
        f"{job_description}"
    )
    try:
        config = genai.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=config)
        data = json.loads(response.text)
        return data.get("skills", [])
    except Exception as e:
        logger.error(f"Gemini API request failed: {e}")
        return []