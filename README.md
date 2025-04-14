# Smart-Garbage-Monitoring
 ## Deployed link : https://kgvsmartgarbagemonitoring.netlify.app/

 🗑️ Smart Garbage Monitoring System – Final Overview
🔧 Project Objective:
To create an efficient, IoT-based garbage monitoring system that automates waste level detection and alerts municipal authorities when bins are nearly full, enhancing the waste management process.

🧩 System Phases:
## 1. Frontend Development:
Web Dashboard for monitoring the status of multiple bins.
Waste Level Indicators (e.g., progress bars, percentage indicators).
Real-Time Graphs for weekly/monthly data tracking.
Alert Display when a bin reaches critical levels (90% full).
Captured Event Logs from sensors (e.g., when waste is added).

## 2. Backend & System Integration:
APIs for receiving sensor data and serving it to the frontend.
Database to log: Bin levels
Timestamps of activity
Alert history
SMS Alert System: Sends notifications to BBMP when bin is over 90% full.
Shortest Path Optimization: Uses bin location and fullness data to determine the most efficient collection route.

## 3. Raspberry Pi Integration:
Ultrasonic Sensor:Measures bin fill level.Detects when garbage is added.
Motion Sensor (PIR):Detects human presence near the bin. Can trigger LED or other actions (e.g., logging usage).
Servo Motor:Automatically opens and closes the lid when motion is detected.
LED Bulb:Provides visual indicator (e.g., lights up when someone approaches or when bin is full).
Cloud Sync:Sends all data to the backend in real time.

# 🌟 Key Features:
Real-time waste level detection using ultrasonic sensor. Automatic lid control via motion detection + servo motor. LED indicator for visual feedback.
Dashboard for centralized monitoring.
SMS alerts to authorities when bin is full.
Route optimization for efficient garbage collection.
