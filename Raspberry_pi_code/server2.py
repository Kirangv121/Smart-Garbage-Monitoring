from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading

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

# Variable to store the latest distance
current_distance = None

# Endpoint to receive distance data
@app.post("/api/update_distance")
async def update_distance(data: dict):
    global current_distance
    if "distance" in data:
        current_distance = data["distance"]
        print(f"Updated distance: {current_distance}")
        return {"message": "Distance updated successfully"}
    return {"error": "Invalid data"}

# Endpoint to get the latest distance data
@app.get("/api/get_data")
async def get_data():
    return {"bin1_distance": current_distance if current_distance is not None else 0}

# Function to Run FastAPI
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    # Start FastAPI server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
