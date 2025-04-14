import RPi.GPIO as GPIO
import time
import requests
from twilio.rest import Client

# Set GPIO Mode
GPIO.setmode(GPIO.BCM)

# Define GPIO Pins
TRIG = 17        # Ultrasonic Trigger
ECHO = 18        # Ultrasonic Echo
SERVO = 14       # Servo Motor
PIR = 15         # PIR Motion Sensor
LED = 21         # LED Indicator

# API Endpoint (Replace with your actual backend IP)
API_URL = "http://130.1.20.165:5000/api/update_distance"

# Twilio Credentials (Replace with your own)
TWILIO_SID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_PHONE = "xxxxxxxxxx"  # Your Twilio phone number
USER_PHONE = "xxxxxxxxxx"    # User’s phone number

# Setup GPIO Pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# Setup Servo Motor
pwm = GPIO.PWM(SERVO, 50)  # Set PWM frequency to 50Hz
pwm.start(0)  # Start PWM with a 0% duty cycle

# Variable to track if an alert has been sent
alert_sent = False

def set_angle(angle):
    """Move servo to a specific angle."""
    duty = (angle / 18) + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    pwm.ChangeDutyCycle(0)

def get_distance():
    """Measure distance using Ultrasonic Sensor."""
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    # Wait for Echo response
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Convert to cm

    return round(distance, 2)

def send_data(distance):
    """Send distance data to FastAPI backend."""
    data = {"distance": distance}
    try:
        response = requests.post(API_URL, json=data, timeout=5)
        print("📡 Server Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("❌ Error sending data:", e)

def send_sms_alert():
    """Send an SMS alert when the bin is 90% full."""
    global alert_sent

    if alert_sent:
        print("⚠️ Alert already sent! No duplicate SMS.")
        return

    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body="🚨 Garbage Alert: Bin is 90% Full! Please take action.",
            from_=TWILIO_PHONE,
            to=USER_PHONE
        )
        print("📩 SMS sent successfully! Message SID:", message.sid)
        alert_sent = True  # Prevent sending duplicate alerts

    except Exception as e:
        print("❌ Error sending SMS:", e)

def check_garbage():
    """Check bin fill level and send an SMS alert when full."""
    global alert_sent

    distance = get_distance()
    print(f"📏 Bin Distance: {distance} cm")

    if distance < 10:  # If bin is 90% full
        GPIO.output(LED, GPIO.HIGH)
        print("⚠️ ALERT: Bin is FULL!")
        send_sms_alert()  # Send SMS alert
    else:
        GPIO.output(LED, GPIO.LOW)
        print("✅ Bin has space.")
        alert_sent = False  # Reset alert when bin is emptied

    return distance

# Initialize Servo Position (Closed)
set_angle(0)

try:
    print("🚀 System Ready... Waiting for Motion & Distance Updates")
    last_motion_state = False  # Track motion state to avoid unnecessary movements

    while True:
        # PIR Motion Detection (Open Lid on Motion)
        if GPIO.input(PIR):  # Motion detected
            if not last_motion_state:
                print("🚶 Motion Detected! Opening Bin")
                set_angle(90)  # Open Bin Lid
                last_motion_state = True
        else:  # No Motion
            if last_motion_state:
                print("🔒 No Motion! Closing Bin")
                set_angle(0)  # Close Bin Lid
                last_motion_state = False

        # Check Bin Fill Level
        distance = check_garbage()
        send_data(distance)  # Send distance to cloud

        time.sleep(3)  # Delay to avoid excessive API calls

except KeyboardInterrupt:
    print("\n🛑 Stopping System...")

finally:
    pwm.stop()
    GPIO.cleanup()
