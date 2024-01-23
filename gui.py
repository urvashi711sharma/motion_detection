import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from motion_detection import MotionDetector

class MotionDetectionGUI:
    def __init__(self, root, motion_detector):
        self.root = root
        self.root.title("Motion Detection App")
        self.motion_detector = motion_detector
        self.motion_detection_active = False
        self.img_tk = None  # Variable to store the ImageTk object

        # Configure root window
        self.root.configure(bg="#333333")  # Dark gray background
        self.create_widgets()

    def create_widgets(self):
        # Create canvas for displaying video frames
        self.canvas = tk.Canvas(self.root, bg="#333333")  # Dark gray canvas background
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create buttons for starting motion detection and quitting the application
        self.start_button = ttk.Button(self.root, text="Start Motion Detection", command=self.toggle_motion_detection, style="TButton")
        self.start_button.pack(pady=10)

        self.quit_button = ttk.Button(self.root, text="Quit", command=self.quit_app, style="TButton")
        self.quit_button.pack(pady=10)

        # Configure button styles
        self.root.option_add('*TButton*background', '#333333')  # Dark gray button background
        self.root.option_add('*TButton*foreground', 'white')  # White font color

    def toggle_motion_detection(self):
        self.motion_detection_active = not self.motion_detection_active
        if self.motion_detection_active:
            self.start_button.config(text="Stop Motion Detection")
            self.start_motion_detection()
        else:
            self.start_button.config(text="Start Motion Detection")

    def start_motion_detection(self):
        def update_display(frame, motion_detected, speed):
            img_pil = Image.fromarray(frame)
            self.img_tk = ImageTk.PhotoImage(img_pil)
            self.canvas.config(width=self.img_tk.width(), height=self.img_tk.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
            
            # Display motion information
            self.display_motion_info(motion_detected, speed)
            
            self.root.update_idletasks()
            self.root.update()

        self.motion_detector.start_motion_detection(update_display)

    def display_motion_info(self, motion_detected, speed):
        # Display motion status
        motion_status = "Motion Detected" if motion_detected else "No Motion Detected"
        self.canvas.create_text(10, 10, anchor=tk.NW, text=motion_status, font=("Arial", 16), fill="black")

        # Display speed
        speed_text = f"Speed: {speed:.2f} pixels/frame"
        self.canvas.create_text(10, 30, anchor=tk.NW, text=speed_text, font=("Arial", 16), fill="black")

    def quit_app(self):
        self.motion_detection_active = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    motion_detector = MotionDetector()
    app = MotionDetectionGUI(root, motion_detector)
    root.attributes('-fullscreen', True)  # Set to fullscreen
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Set window size to fullscreen
    root.mainloop()