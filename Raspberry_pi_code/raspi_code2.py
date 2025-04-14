import RPi.GPIO as GPIO
import time
import requests

# Define GPIO Pins
TRIG = 17
ECHO = 18

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# FastAPI Server URL (Replace with your actual backend IP)
API_URL = "http://130.1.20.165:5000/api/update_distance"

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
    data = {"distance": distance}
    try:
        response = requests.post(API_URL, json=data, timeout=5)
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error sending data:", e)

try:
    while True:
        distance = get_distance()
        if distance:
            print(f"Distance: {distance} cm")

            # Send data to the server
            send_data(distance)

        else:
            print("Invalid sensor reading. Skipping...")

        time.sleep(3)  # Send data every 3 seconds

except KeyboardInterrupt:
    print("\nStopping...")
    GPIO.cleanup()
