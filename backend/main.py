from fastapi import FastAPI, UploadFile, File # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
# from fastapi.responses import HTMLResponse # <-- You can remove this if read_root is deleted
from fastapi.staticfiles import StaticFiles # type: ignore # <-- ADD THIS IMPORT
from ai_model import analyze_image
import shutil
import uuid
import os


app = FastAPI(title="AI Food Detector API")
# Define paths correctly relative to main.py
# In main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Note: UPLOAD_DIR is set to "uploads"

# Add this print statement when the server starts
print(f"Server starting in directory: {BASE_DIR}")
print(f"Files should be saved to: {os.path.join(BASE_DIR, UPLOAD_DIR)}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Setup CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MOUNT STATIC FILES 
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")

# In main.py
@app.post("/detect")
async def detect_food(image: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}-{image.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    try:
        # 1. File Saving
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # 2. IMMEDIATE SUCCESS RETURN (Bypasses analyze_image)
        return {
            "status": "success",
            "freshness": "File Receipt Confirmed!",
            "confidence": f"Saved as: {filename}",
            "uploaded_file": filename
        }

    except Exception as e:
        print(f"An error occurred during detection: {e}")
        return {"status": "error", "message": f"Processing failed: {e}"}