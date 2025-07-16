from fastapi import APIRouter
from pydantic import BaseModel
import google.generativeai as genai
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic model for the request body
class SkillExtractionRequest(BaseModel):
    raw_text: str

# Configure Gemini API with hard-coded key (temporary)
genai.configure(api_key="AIzaSyAOo9CuBW6r6DZa7qwURn10ztzW7_pjNZs")
model = genai.GenerativeModel('gemini-2.5-flash')

@router.post("/extract-skills")
async def extract_skills(request: SkillExtractionRequest):
    raw_text = request.raw_text
    logger.info(f"Extracting skills from text: {raw_text[:50]}...")
    # Simple prompt to extract skills
    prompt = f"""
    Extract a list of skills from this CV text.
    
    Ensure your reponse is as so: "[skill1, skill2, skill3, ...]".
    
    It is of most importance that you do not include any other text in your response.

    CV Text: {raw_text}
    """

    # Generate content with Gemini
    response = model.generate_content(prompt)
    logger.info(f"Raw Gemini response: {response.text}")
    return response.text