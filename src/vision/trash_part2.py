import ultralytics
from ultralytics import YOLO
import cv2
import serial
import time
# load hyper tuned model
model = YOLO('batch2.pt')

# Initialize Arduino/ESP32
arduino = serial.Serial('COM3', 9600)  # Linux/macOS (use 'COM3' for Windows)
time.sleep(2)  # Allow time for Arduino to initialize

# establish and open webcam feed
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot read camera")
        exit(2)

    # pass frame through model
    # frame_resized = cv2.resize(frame, (640, 480))
    res = list(model(source=0, stream=True, show=True, verbose=False))

        # Check if any object was detected
    detected = False

    for result in res:
        if len(result.boxes) > 0:  # If detections exist
            detected = True
            cv2.imshow('Stream', result.plot())  # Show bounding boxes

    # Send signal to Arduino
    if detected:

        arduino.write(b'1')  # Send "1" when object is detected
    else:
        arduino.write(b'0')  # Send "0" when no object is detected

    #Display resulting frame
    # cv2.imshow('Stream', res[0].plot())  # Now indexing works

    # Break loop on 'q' for quit
    if cv2.waitKey(1) == ord('q'):
        break





