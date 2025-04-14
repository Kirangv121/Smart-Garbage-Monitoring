from flask import Flask, Response, render_template_string
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

# Configure and start the camera
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(video_config)
picam2.start()

def generate_frames():
    """Capture frames continuously and encode them as JPEG."""
    while True:
        # Capture frame as a numpy array
        frame = picam2.capture_array()
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        # Yield the output frame in byte format using the MJPEG format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Route to display the live video stream
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Main page with HTML that embeds the video stream
@app.route('/')
def index():
    html = """
    <html>
      <head>
        <title>Raspberry Pi Live Stream</title>
      </head>
      <body>
        <h1>Live Camera Feed</h1>
        <img src="/video_feed" width="640" height="480">
      </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    # Run the Flask app on all interfaces at port 8000
    app.run(host='0.0.0.0', port=8000, threaded=True)
