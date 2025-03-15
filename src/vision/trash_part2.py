from ultralytics import YOLO
import cv2

# load hyper tuned model
model = YOLO('../../yolov8n.pt')

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
    res = list(model(source=0, stream=True, show=True))

    #Display resulting frame
    #res = list(model(frame))  # Convert generator to list
    cv2.imshow('Stream', res[0].plot())  # Now indexing works

    # Break loop on 'q' for quit
    if cv2.waitKey(1) == ord('q'):
        break