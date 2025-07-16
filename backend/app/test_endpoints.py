import requests
import logging

# Configure basic logging with a clean format
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Hardcoded PDF path (update to a valid file if needed)
pdf_path = r"C:\Users\human\Desktop\1.pdf"

# URL of the local FastAPI server
base_url = "http://localhost:8000/api"

if __name__ == "__main__":
    # Header for the test run
    logger.info("=== Starting Endpoint Tests ===")

    # Step 1: Upload the PDF to /upload-cv
    logger.info("--- Step 1: Uploading PDF to /upload-cv ---")
    logger.info(f"Attempting to upload file: {pdf_path}")
    try:
        with open(pdf_path, 'rb') as file:
            files = {'file': file}
            upload_response = requests.post(f"{base_url}/upload-cv", files=files)

        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            logger.info("Upload successful!")
            logger.info(f"Extracted Text: {upload_data['extracted_text']}")
            raw_text = upload_data.get("extracted_text")
        else:
            logger.error(f"Upload failed with status {upload_response.status_code}")
            logger.error(f"Error details: {upload_response.text}")
            raw_text = None
    except Exception as e:
        logger.error(f"Upload failed due to exception: {str(e)}")
        raw_text = None

    # Step 2: Extract raw Gemini response from /extract-skills
    if raw_text:
        logger.info("--- Step 2: Getting Raw Gemini Response from /extract-skills ---")
        logger.info(f"Sending text for raw response: {raw_text[:50]}...")
        headers = {'Content-Type': 'application/json'}
        data = {"raw_text": raw_text}
        skills_response = requests.post(f"{base_url}/extract-skills", json=data, headers=headers)

        if skills_response.status_code == 200:
            # Note: The raw Gemini response is logged by the server, so we fetch it indirectly
            logger.info("Raw Gemini response fetched successfully!")
            logger.info(f"Raw Response: {skills_response.text}")  # Display the server's returned response
        else:
            logger.error(f"Raw response fetch failed with status {skills_response.status_code}")
            logger.error(f"Error details: {skills_response.text}")
    else:
        logger.info("--- Step 2: Skipping raw response (no text from upload) ---")

    # Footer for the test run
    logger.info("=== Endpoint Tests Completed ===")