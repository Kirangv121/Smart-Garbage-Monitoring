from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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

# Store the latest distance data
current_distance = None
image_captured = False  # Track if an image was captured

@app.post("/api/update_distance")
async def update_distance(data: dict):
    """Receive and update bin distance."""
    global current_distance, image_captured
    current_distance = data.get("distance")

    if current_distance is not None:
        print(f"Updated distance: {current_distance} cm")

        # Check if bin is 90% full and mark image capture
        if current_distance <= 4 and not image_captured:  # Assuming 4cm = 90% full
            image_captured = True  # Mark as captured
            return {"message": "Distance updated, bin is 90% full! Capture image now."}

        # Reset image capture flag when waste level decreases
        if current_distance > 6:
            image_captured = False  

        return {"message": "Distance updated successfully"}
    
    return {"error": "Invalid data received"}

@app.get("/api/get_data")
async def get_data():
    """Provide bin distance to frontend."""
    return {"bin1_distance": current_distance or 0, "image_captured": image_captured}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5000, reload=True)
