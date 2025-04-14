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

# Backend API URL (Replace with your actual backend URL)
API_URL = "http://130.1.74.196:5000/api/update_distance"



def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Convert to cm
    return round(distance, 2)

try:
    while True:
        distance = get_distance()
        print(f"Distance: {distance} cm")

        # Send data to backend
        data = {"distance": distance}
        response = requests.post(API_URL, json=data)
        print("Response:", response.text)

        time.sleep(5)  # Send data every 5 seconds

except KeyboardInterrupt:
    print("Stopping...")
    GPIO.cleanup()
