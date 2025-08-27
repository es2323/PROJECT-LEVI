# backend/app/models.py
from pydantic import BaseModel
from typing import List, Dict, Optional

class CvSkill(BaseModel):
    name: str
    proficiency: int
    confidence: int

class QuestionnaireAnswers(BaseModel):
    sector: Optional[str] = None
    roles: Optional[List[str]] = []
    ambition: Optional[str] = None
    passion: Optional[List[str]] = []
    confidence: Optional[str] = None
    learningStyle: Optional[List[str]] = []
    techPreference: Optional[str] = None
    workPace: Optional[str] = None

class FinalPayload(BaseModel):
    cv_skills: List[CvSkill]
    questionnaire_answers: QuestionnaireAnswers