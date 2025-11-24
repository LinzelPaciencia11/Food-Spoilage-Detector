import os
import random
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import shutil

# Initialize the FastAPI application
app = FastAPI()

# --- FIX IS HERE ---
# Correctly configure CORS to allow requests from any origin ("*") 
# and the necessary HTTP methods (POST, GET, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], # Allow POST for the /analyze endpoint
    allow_headers=["*"],
)
# --- END FIX ---

# Configuration
UPLOAD_DIR = "uploads"
# Create the uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper function for dummy analysis
def analyze_image(image_path):
    """
    Dummy AI analysis function. 
    It simulates an AI model by returning a random freshness result.
    It also cleans up the file after analysis.
    """
    options = ["Fresh", "Slightly Old", "Spoiled"]
    result = random.choice(options)

    # Clean up the file after analysis
    if os.path.exists(image_path):
        os.remove(image_path)
    
    # Return a structured result
    return {
        "freshness": result, 
        "confidence": round(random.uniform(0.70, 0.99), 2)
    }

@app.post("/analyze")
async def detect_food(image: UploadFile = File(...)):
    """Save the uploaded file and return its path."""
    try:
        # Create unique filename
        filename = f"{uuid.uuid4()}-{image.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        options = ["Fresh", "Slightly Old", "Spoiled"]
        result = random.choice(options)

        # Save file
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Return success response
        return {
            "status": "success",
            "freshness": result,
            "uploaded_file": filename,
            "path": filepath,
            "confidence": round(random.uniform(0.70, 0.98), 2),
        }

    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}