import cv2
import serial  # Allows communication with Arduino
from ultralytics import YOLO


# Connect to Arduino (update the COM port for Windows or /dev/ttyUSB0 for Linux)
arduino = serial.Serial("COM3", 9600, timeout=1)

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO on the frame
    results = model(frame)

    detected_class = None  # Store detected trash type
    for r in results:
        for c in r.names:
            if "bottle" in c or "plastic" in c:
                detected_class = "1"  # Plastic
            elif "paper" in c or "cardboard" in c:
                detected_class = "2"  # Paper
            elif "can" in c or "metal" in c:
                detected_class = "3"  # Metal

    if detected_class:
        arduino.write(detected_class.encode())  # Send signal to Arduino

    # Show results on screen
    cv2.imshow("Trash Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
arduino.close()
