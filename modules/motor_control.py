# modules/motor_control.py
import time

class MotorController:
    def __init__(self, left_pin_fwd=17, left_pin_bwd=18, right_pin_fwd=22, right_pin_bwd=23):
        self.left_fwd = left_pin_fwd
        self.left_bwd = left_pin_bwd
        self.right_fwd = right_pin_fwd
        self.right_bwd = right_pin_bwd
        self.current_state = "STOP"
        print("[MotorController] Initialized pins for left and right motors.")

    def forward(self, duration=None):
        if self.current_state != "FORWARD":
            print("[MotorController] Moving FORWARD...")
            self.current_state = "FORWARD"
        if duration:
            time.sleep(duration)
            self.stop()

    def backward(self, duration=None):
        if self.current_state != "BACKWARD":
            print("[MotorController] Moving BACKWARD...")
            self.current_state = "BACKWARD"
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_left(self, duration=None):
        if self.current_state != "LEFT":
            print("[MotorController] Turning LEFT...")
            self.current_state = "LEFT"
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_right(self, duration=None):
        if self.current_state != "RIGHT":
            print("[MotorController] Turning RIGHT...")
            self.current_state = "RIGHT"
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        if self.current_state != "STOP":
            print("[MotorController] Motors STOPPED.")
            self.current_state = "STOP"