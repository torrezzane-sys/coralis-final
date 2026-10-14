# modules/sensors.py
import random

class WaterQualityAndGPS:
    def __init__(self):
        print("[Sensors] Running in simulation mode.")

    def read_all(self):
        return {
            "ph": round(random.uniform(6.8, 7.6), 2),
            "turbidity": round(random.uniform(2.0, 5.5), 2),
            "temperature": round(random.uniform(25.0, 28.5), 1),
            "gps": {
                "latitude": 8.2279 + random.uniform(-0.001, 0.001),
                "longitude": 124.2453 + random.uniform(-0.001, 0.001)
            }
        }