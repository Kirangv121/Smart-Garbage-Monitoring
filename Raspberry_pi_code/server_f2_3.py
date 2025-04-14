from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import threading

app = FastAPI()

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables to store bin data
BIN_HEIGHT = 50  # Example: total bin height in cm (adjust based on actual bin size)
current_distance = None  # Distance measured by the ultrasonic sensor

# Request model for updating distance
class DistanceUpdate(BaseModel):
    distance: float

# Response model for bin data
class BinDataResponse(BaseModel):
    bin_level: float

# Endpoint to receive distance data from the ultrasonic sensor
@app.post("/api/update_distance")
async def update_distance(data: DistanceUpdate):
    global current_distance
    current_distance = data.distance
    print(f"Updated distance: {current_distance} cm")
    return {"message": "Distance updated successfully"}

# Endpoint to get the latest bin level data
@app.get("/api/get_data", response_model=BinDataResponse)
async def get_data():
    global current_distance
    if current_distance is not None:
        # Calculate bin level percentage: (BIN_HEIGHT - distance) / BIN_HEIGHT * 100
        bin_level = max(0, min(100, ((BIN_HEIGHT - current_distance) / BIN_HEIGHT) * 100))
    else:
        bin_level = 0  # Default to 0% if no data received

    return {"bin_level": bin_level}

# Function to run FastAPI server
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    # Start FastAPI server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
