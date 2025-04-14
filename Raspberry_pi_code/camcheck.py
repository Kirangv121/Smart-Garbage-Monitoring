from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from picamera2 import Picamera2

# Initialize FastAPI App
app = FastAPI()

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pi Camera
picam2 = Picamera2()
picam2.start()

# Ensure static folder exists
os.makedirs("static", exist_ok=True)
IMAGE_PATH = "static/bin_image.jpg"

@app.get("/api/get_data")
def get_data():
    """Simulated bin distance (replace with real sensor data)."""
    distance = 15  # Example distance in cm
    return {"bin1_distance": distance}

@app.post("/api/capture_image")
def capture_image():
    """Capture an image and save it to the static folder."""
    picam2.capture_file(IMAGE_PATH)
    return {"message": "Image captured successfully"}

@app.get("/static/bin_image.jpg")
def serve_image():
    """Serve the latest bin image."""
    return FileResponse(IMAGE_PATH)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
