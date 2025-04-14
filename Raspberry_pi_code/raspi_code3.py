import RPi.GPIO as GPIO
import time
import requests
import cv2
from datetime import datetime

# Define GPIO Pins
TRIG = 17
ECHO = 18

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# FastAPI Server URL (Replace with your actual backend IP)
API_URL = "http://130.1.20.165:5000/api/update_distance"

# Camera Setup
camera = cv2.VideoCapture(0)  # Use Raspberry Pi Camera
image_captured = False  # Track if an image was captured

def get_distance():
    """Measure distance using Ultrasonic Sensor."""
    try:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        pulse_start = time.time()
        pulse_end = time.time()

        # Wait for ECHO response
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        # Calculate distance
        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 34300) / 2  # Convert to cm
        
        # Ignore invalid readings (out of sensor range)
        if 2 <= distance <= 400:
            return round(distance, 2)
        else:
            return None
    except Exception as e:
        print(f"Error reading sensor: {e}")
        return None

def send_data(distance):
    """Send distance data to FastAPI backend."""
    global image_captured
    data = {"distance": distance}

    try:
        response = requests.post(API_URL, json=data, timeout=5)
        print("Response:", response.text)

        # If bin is 90% full and image is not yet captured
        if distance <= 4 and not image_captured:  # Assuming 4cm means 90% full
            capture_image()
            image_captured = True  # Mark image as captured
        
        # Reset flag if bin level decreases
        if distance > 6:
            image_captured = False  

    except requests.exceptions.RequestException as e:
        print("Error sending data:", e)

def capture_image():
    """Capture image when bin is 90% full."""
    ret, frame = camera.read()
    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"bin_images/bin_full_{timestamp}.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Image captured: {image_path}")
    else:
        print("Error: Unable to capture image")

try:
    while True:
        distance = get_distance()
        if distance:
            print(f"Distance: {distance} cm")
            send_data(distance)
        else:
            print("Invalid sensor reading. Skipping...")

        time.sleep(3)  # Send data every 3 seconds

except KeyboardInterrupt:
    print("\nStopping...")
    GPIO.cleanup()
    camera.release()
    cv2.destroyAllWindows()
