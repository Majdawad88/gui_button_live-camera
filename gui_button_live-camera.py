#git clone https://github.com/Majdawad88/gui_button_live-camera.git
import tkinter as tk
from tkinter import Button
import cv2
from picamera2 import Picamera2
import threading
import sys

class CameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Pi Camera Control")
        self.window.geometry("300x200")
        
        self.picam2 = Picamera2()
        self.is_running = False
        
        # UI Button
        self.btn = Button(window, text="Start Video", command=self.toggle_camera, 
                          width=15, height=3, bg='green', fg='white', font=('Arial', 12, 'bold'))
        self.btn.pack(expand=True)

        self.window.protocol("WM_DELETE_WINDOW", self.cleanup)

    def video_loop(self):
        """This function runs in the background and shows the video in an OpenCV window"""
        try:
            config = self.picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
            self.picam2.configure(config)
            self.picam2.start()

            while self.is_running:
                frame = self.picam2.capture_array()
                # OpenCV windows ARE visible in Raspberry Pi Connect/VNC
                cv2.imshow("Live Video Feed", frame)
                
                # Check for 1ms delay to keep window responsive
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cv2.destroyAllWindows()
            self.picam2.stop()
        except Exception as e:
            print(f"Video Error: {e}")
            self.is_running = False

    def toggle_camera(self):
        if not self.is_running:
            self.is_running = True
            self.btn.config(text="Stop Video", bg='red')
            # Start the background thread
            threading.Thread(target=self.video_loop, daemon=True).start()
        else:
            self.is_running = False
            self.btn.config(text="Start Video", bg='green')

    def cleanup(self):
        self.is_running = False
        self.picam2.close()
        cv2.destroyAllWindows()
        self.window.destroy()
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
