# main.py - Integrated Motors, Sensors, & AI Camera Stream (Plug-and-Play)
from modules.motor_control import MotorController
from modules.sensors import WaterQualityAndGPS
from modules.camera import VideoStreamer
import keyboard
import time
import threading
import cv2

print("Initializing C.O.R.A.L.I.S. Full System...")
motors = MotorController()
sensors = WaterQualityAndGPS()

# Camera auto-detects your webcam now, and loads your custom YOLO coral model automatically
camera = VideoStreamer(model_path=r"C:\yolo\my_model\my_model.pt")

# Flag to control background loops
running = True

def sensor_telemetry_loop():
    """Background worker for sensor logs."""
    global running
    while running:
        sensor_data = sensors.read_all()
        print("\n--- [TELEMETRY UPDATE] ---")
        print(f" GPS: {sensor_data['gps']}")
        print(f" Temp: {sensor_data['temperature']} °C | pH: {sensor_data['ph']} | Turbidity: {sensor_data['turbidity']} NTU")
        print("----------------------------\n")
        
        for _ in range(40):
            if not running:
                break
            time.sleep(0.1)

# Start sensor telemetry in a background thread
telemetry_thread = threading.Thread(target=sensor_telemetry_loop, daemon=True)
telemetry_thread.start()

print("\n--- SYSTEM READY ---")
print("  Hold [Up/Down/Left/Right] -> Drive Motors")
print("  Press [Esc] or 'q'        -> Quit Program")
print("----------------------------------------------------\n")

try:
    while running:
        # 1. Grab and show the live AI camera feed in a window
        frame = camera.get_frame()
        cv2.imshow("C.O.R.A.L.I.S. Live AI Feed", frame)
        
        # If user presses 'q' on the video window, break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 2. Real-time keyboard checking for driving
        if keyboard.is_pressed('up'):
            motors.forward()
        elif keyboard.is_pressed('down'):
            motors.backward()
        elif keyboard.is_pressed('left'):
            motors.turn_left()
        elif keyboard.is_pressed('right'):
            motors.turn_right()
        elif keyboard.is_pressed('esc'):
            break
        else:
            motors.stop()
        
        time.sleep(0.03)

except Exception as e:
    print(f"\nError: {e}")

finally:
    # Safe shutdown
    print("\nShutting down system safely...")
    running = False
    motors.stop()
    camera.release()
    print("Goodbye!")