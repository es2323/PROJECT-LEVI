from pydantic import BaseModel
from typing import List

class UserModel(BaseModel):
    skills: List[str] = []
    cv_text: str  # Required string to store raw CV text

    class Config:
        arbitrary_types_allowed = True  # Allow flexibility for MongoDB integration
        json_encoders = {}  # No specific encoders needed since no ObjectId is managed here

# Example document structure (not enforced, kept flexible)
user_example = {
    "skills": ["python", "css", "django"],
    "cv_text": "Sample CV text here"
}
