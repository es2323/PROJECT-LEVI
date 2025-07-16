from fastapi import APIRouter, UploadFile, File
import pdfplumber
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    logger.info(f"Endpoint hit with file: {file.filename}")  # Debug log
    try:
        # Extract text from PDF
        with pdfplumber.open(file.file) as pdf:
            text = ""
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
            if not text:
                text = "No text extracted"

        # Log the extracted text to the console
        # Still need to add link to /api/extract-skills endpoint for seamless integration
        logger.info(f"Extracted text: {text}")

        return {"message": "Text extracted", "extracted_text": text}

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return {"message": "Error", "error": str(e)}