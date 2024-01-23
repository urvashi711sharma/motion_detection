# motion_detection.py
import cv2
import imutils

class MotionDetector:
    def __init__(self, resize_width=1200, area_threshold=1000):  # Adjusted parameters
        self.resize_width = resize_width
        self.area_threshold = area_threshold
        self.first_frame = None
        self.prev_center = None
        self.motion_history = []

    def calculate_speed(self, current_center):
        if self.prev_center is None:
            return 0.0

        distance = ((current_center[0] - self.prev_center[0])**2 + (current_center[1] - self.prev_center[1])**2)**0.5
        speed = distance / 2.0  # Adjusted factor

        return speed

    def start_motion_detection(self, motion_callback):
        cap = cv2.VideoCapture(0)

        while True:
            _, frame = cap.read()

            if frame is None:
                print("Error reading frame.")
                break

            frame = imutils.resize(frame, width=self.resize_width)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

            if self.first_frame is None:
                self.first_frame = blurred_frame
                continue

            frame_diff = cv2.absdiff(self.first_frame, blurred_frame)
            thresh_frame = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
            dilated_frame = cv2.dilate(thresh_frame, None, iterations=2)

            contours = cv2.findContours(dilated_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            motion_detected = False

            for contour in contours:
                if cv2.contourArea(contour) < self.area_threshold:
                    continue

                (x, y, w, h) = cv2.boundingRect(contour)
                center = (int(x + w / 2), int(y + h / 2))

                speed = self.calculate_speed(center)
                print(f"Speed: {speed:.2f} pixels/frame")

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, center, 5, (0, 255, 0), -1)
                motion_detected = True

                self.prev_center = center

            self.motion_history.append(int(motion_detected))

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            motion_callback(img_rgb, motion_detected, speed)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
