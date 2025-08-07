import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Get API keys from environment variables
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

logger = logging.getLogger(__name__)

def get_job_listings(job_title: str, location: str = "gb", results_per_page: int = 5) -> list[str]:
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        logger.error("Adzuna API credentials are not set in the .env file.")
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
        logger.info(f"Fetched {len(descriptions)} descriptions for '{job_title}' from Adzuna.")
        return descriptions
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from Adzuna: {e}")
        return []