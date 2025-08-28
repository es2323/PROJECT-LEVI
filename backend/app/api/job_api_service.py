import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

logger = logging.getLogger(__name__)

def get_job_listings(job_title: str, location: str = "gb", results_per_page: int = 5) -> list[str]:
    """Fetches job descriptions from the Adzuna API for a given job title."""
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        logger.error("Adzuna API credentials not configured.")
        return []

    api_url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_APP_KEY,
        'what': job_title,
        'results_per_page': results_per_page,
        'content-type': 'application/json'
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        descriptions = [job['description'] for job in data.get('results', [])]
        return descriptions
    except requests.exceptions.RequestException as e:
        logger.error(f"Adzuna API request failed: {e}")
        return []