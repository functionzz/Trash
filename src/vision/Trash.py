import serial
import time
from ultralytics import YOLO

# Open Serial communication with Arduino (adjust COM port for Windows)
arduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
time.sleep(2)  # Wait for connection

# Load YOLO model
model = YOLO("yolov8n.pt")

# Run detection on an image or camera feed
results = model("trash_image.jpg")

# Parse detected objects
for r in results:
    for obj in r.names:
        if "plastic" in obj:
            arduino.write(b'1')  # Send signal to Arduino for plastic
        elif "paper" in obj:
            arduino.write(b'2')  # Send signal for paper
        elif "metal" in obj:
            arduino.write(b'3')  # Send signal for metal
