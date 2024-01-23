import cv2
import time

class MotionSpeedDetector:
    def __init__(self):
        self.prev_time = time.time()

    def calculate_speed(self, distance, time_interval):
        if time_interval == 0:
            return 0
        return distance / time_interval

    def update_time(self):
        current_time = time.time()
        time_interval = current_time - self.prev_time
        self.prev_time = current_time
        return time_interval

    def detect_motion_speed(self, x, y, w, h, resize_width):
        distance = w  # Assume distance is the width of the bounding box
        time_interval = self.update_time()
        speed = self.calculate_speed(distance, time_interval)
        return speed
