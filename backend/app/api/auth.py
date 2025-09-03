# backend/app/api/auth.py

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import httpx
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Load your credentials from environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/api/auth/google/callback"

@router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    """
    This endpoint is hit after the user authenticates with Google.
    It exchanges the authorization code for an access token and user info.
    """
    # 1. Get the authorization code from the URL
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found.")

    # 2. Exchange the code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    async with httpx.AsyncClient() as client:
        try:
            token_response = await client.post(token_url, data=token_data)
            token_response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            token_json = token_response.json()
            access_token = token_json.get("access_token")

            if not access_token:
                raise HTTPException(status_code=400, detail="Access token not found in response from Google.")

            # 3. Use the access token to get the user's profile info
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}
            user_info_response = await client.get(user_info_url, headers=headers)
            user_info_response.raise_for_status()
            user_info = user_info_response.json()
            
            logger.info(f"Successfully fetched user info: {user_info.get('email')}")

            # --- TODO: Database and Session Logic ---
            # 4. Find or create a user in your database with the user_info['id'] or user_info['email']
            # 5. Create a session for that user (using your fastapi-sessions)
            # 6. Attach the session cookie to the response
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred during Google OAuth flow: {e.response.text}")
            raise HTTPException(status_code=500, detail="Error communicating with Google.")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    # 7. Redirect the user back to your frontend application
    # This sends them back to the main page after a successful login.
    return RedirectResponse(url="http://localhost:5173")