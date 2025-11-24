import os
import random # <--- Make sure this is imported!


def analyze_image(image_path):
    """
    Mocks the AI analysis of an image for freshness.
    In a real app, this would load the image from image_path and run the ML model.
    """
    # Dummy logic to simulate an ML model prediction
    options = ["Fresh", "Slightly Old", "Spoiled"]
    result = random.choice(options)
    
    # Clean up the file after analysis (optional, but good practice)
    if os.path.exists(image_path):
        os.remove(image_path)
    
    return {
        "freshness": result,
        "confidence": round(random.uniform(0.70, 0.98), 2)
    }
# --------