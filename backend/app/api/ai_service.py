import json
import google.generativeai as genai
import logging
import os
from dotenv import load_dotenv
from typing import Dict, List, Any

load_dotenv()
GEMINI_API_KEY = os.getenv("GENAI_API_KEY")

# Configure the library with your API key.
if not GEMINI_API_KEY:
    raise ValueError("GENAI_API_KEY not found in environment variables.")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash-latest')
logger = logging.getLogger(__name__)


def extract_skills_from_cv(cv_text: str) -> List[Dict[str, Any]]:
    """Uses Gemini to extract a structured list of skills from CV text."""
    if not cv_text:
        return []

    prompt = f"""
    You are an expert recruitment data analyst. Analyze the provided CV text and extract the candidate's skills.
    Your response MUST be a valid JSON object with a single top-level key "skills".
    The "skills" key must hold a LIST of objects.
    Each object in the list must represent a single skill and have the following keys: "name", "proficiency", "experience", "details".
    - "name": The name of the skill (e.g., "Python"). This is mandatory.
    - "proficiency": A rating like "Beginner", "Intermediate", "Advanced", or "Expert".
    - "experience": A string representing years of experience if available (e.g., "2 years"), otherwise null.
    - "details": A concise sentence describing the context of the skill from the CV.

    Example response format:
    {{
      "skills": [
        {{
          "name": "Python",
          "proficiency": "Advanced",
          "experience": "2 years",
          "details": "Developed a machine learning recommendation system using NumPy and Pandas."
        }}
      ]
    }}

    CV Text:
    {cv_text}
    """
    try:
        config = genai.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=config)
        data = json.loads(response.text)
        return data.get("skills", [])
    except Exception as e:
        logger.error(f"Gemini CV skill extraction failed: {e}")
        return []


def extract_skills_from_job_description(job_description: str) -> list[str]:
    """Extracts a simple list of raw skills from a single job description."""
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
        logger.error(f"Gemini job skill extraction failed: {e}")
        return []


def synthesize_skills(raw_skills_by_role: Dict[str, List[str]]) -> Dict[str, Any]:
    """Takes a dictionary of raw skills and creates a structured analysis."""
    raw_skills_json = json.dumps(raw_skills_by_role, indent=2)
    prompt = f"""
    You are an expert technical recruiter and data analyst.
    Analyze the following JSON object, which contains lists of skills extracted from multiple job ads for different roles.
    Your task is to synthesize this raw data into a structured JSON object.

    The final JSON object MUST have two top-level keys:
    1. "skills_by_role": An object where each key is a job role from the input. The value for each key should be a list of the most important, unique skills for that role.
    2. "common_skills": A list of skills that appear frequently across ALL the different job roles.

    Here is the raw skill data:
    {raw_skills_json}

    Provide only the final, structured JSON object in your response.
    Example response format:
    {{
      "skills_by_role": {{
        "Quantitative Developer": ["C++", "Python", "Financial Modeling"],
        "Backend Engineer": ["Java", "Python", "AWS", "SQL"]
      }},
      "common_skills": ["Python"]
    }}
    """
    try:
        config = genai.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=config)
        synthesized_data = json.loads(response.text)
        return synthesized_data
    except Exception as e:
        logger.error(f"Gemini skill synthesis failed: {e}")
        return {"skills_by_role": {}, "common_skills": []}