import os
import random
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

# Initialize the FastAPI application
app = FastAPI()

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
async def analyze(file: UploadFile = File(...)):
    # --- START of the correctly indented function body ---
    
    # 1. Define the file path where the uploaded file will be saved
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # 2. Save the uploaded file asynchronously
        # The 'await' call MUST be inside this indented block
        with open(file_path, "wb") as f:
            # file.read() is an awaitable method for UploadFile
            f.write(await file.read())

        # 3. Run the AI model (synchronous operation)
        result = analyze_image(file_path)

        # 4. Return the result
        return JSONResponse({"analysis": result})

    except Exception as e:
        # 5. Handle errors and ensure file cleanup if saving failed
        if os.path.exists(file_path):
            os.remove(file_path)
        return JSONResponse({"error": f"An error occurred during analysis: {e}"}, status_code=500)

    # --- END of the function body ---