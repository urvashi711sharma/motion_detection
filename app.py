import tkinter as tk
from gui import MotionDetectionGUI
from motion_detection import MotionDetector

if __name__ == "__main__":
    root = tk.Tk()
    motion_detector = MotionDetector()
    app = MotionDetectionGUI(root, motion_detector)
    root.mainloop()
