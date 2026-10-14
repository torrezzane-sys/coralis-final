# modules/camera.py - Robust Camera Streamer
import cv2
import numpy as np

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

class VideoStreamer:
    def __init__(self, model_path=None):
        print("[Camera] Initializing video feed...")
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            print("[Camera Warning] Could not open webcam index 0!")
            self.is_active = False
        else:
            print("[Camera] Live video feed active successfully!")
            self.is_active = True

        self.model = None
        if YOLO_AVAILABLE and model_path:
            try:
                print(f"[AI] Loading YOLO coral model from: {model_path}")
                self.model = YOLO(model_path)
                print("[AI] Coral model loaded successfully!")
            except Exception as e:
                print(f"[AI Error] Failed to load YOLO model: {e}")

    def get_frame(self):
        if not self.is_active or self.cap is None:
            # Return a bright red frame with text so you know it's a camera error
            error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            error_frame[:] = (0, 0, 150) # Red background
            cv2.putText(error_frame, "CAMERA FEED ERROR / BLOCKED", (50, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            return error_frame

        ret, frame = self.cap.read()
        if not ret or frame is None:
            gray_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(gray_frame, "WAITING FOR FRAME...", (150, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            return gray_frame

        # Run YOLO inference if model is loaded
        if self.model is not None:
            try:
                results = self.model(frame, conf=0.4, verbose=False)
                return results[0].plot()
            except Exception as e:
                print(f"Inference error: {e}")
                return frame

        return frame

    def release(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()