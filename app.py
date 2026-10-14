# app.py
from flask import Flask, render_template, Response, jsonify, request
import cv2
import threading
import webview
from modules.sensors import WaterQualityAndGPS
from modules.camera import VideoStreamer  # <-- Using your custom camera module!

# Try importing RPi.GPIO (Only works on Raspberry Pi, safe-guards Windows simulation)
try:
    import RPi.GPIO as GPIO
    IS_PI = True
except ImportError:
    IS_PI = False

app = Flask(__name__)

# Initialize sensors and camera streamer (pass your custom YOLO model path here if desired)
sensors = WaterQualityAndGPS()
camera = VideoStreamer(model_path=None)

# L298N Pin Configuration (BCM numbering)
ENA = 17
IN1 = 22
IN2 = 23
IN3 = 24
IN4 = 25
ENB = 27

def setup_hardware():
    if IS_PI:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in [ENA, IN1, IN2, IN3, IN4, ENB]:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        print("[Hardware] L298N GPIO pins initialized successfully.")
    else:
        print("[Hardware] Running on Windows (Simulation Mode for GPIO).")

setup_hardware()

# Motor control logic for L298N
def set_motors(action):
    if not IS_PI:
        print(f"[SIMULATION] Motor Action: {action}")
        return

    if action == 'forward':
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    elif action == 'backward':
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    elif action == 'left':
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    elif action == 'right':
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    elif action == 'stop':
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)

def generate_frames():
    """Pulls frames from your camera.py module and streams them via MJPEG"""
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        
        # Resize for consistent streaming bandwidth if needed
        frame = cv2.resize(frame, (640, 480))
        
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def get_data():
    sensor_data = sensors.read_all()
    return jsonify(sensor_data)

@app.route('/control', methods=['POST'])
def control_motors():
    data = request.get_json()
    action = data.get('action')
    set_motors(action)
    return jsonify({"status": "success", "action": action})

def start_flask():
    # Host on '0.0.0.0' so other devices (like your laptop across the CPE210 bridge) can connect!
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()

    # Pywebview opens the local desktop UI window on the Pi
    webview.create_window('C.O.R.A.L.I.S. Control Center', 'http://127.0.0.1:5000', width=1280, height=768)
    webview.start()