import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model (replace 'yolov8n.pt' with the desired model variant)
model = YOLO("weights/best_800.pt")  # load a pretrained model (recommended for training)

# Initialize global variables for ROI selection
ref_point = []
cropping = False
roi_selected = False


# Mouse callback function to define the ROI
def click_and_crop(event, x, y, flags, param):
    global ref_point, cropping, roi_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        frame_copy = frame.copy()
        cv2.rectangle(frame_copy, ref_point[0], (x, y), (0, 255, 0), 2)
        cv2.imshow("Video", frame_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cropping = False
        roi_selected = True
        cv2.rectangle(frame, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("Video", frame)


# Function to run YOLOv8 predictions and draw bounding boxes
def yolo_predict(frame):
    height, width = frame.shape[:2]

    # Run YOLOv8 inference on the frame
    results = model(frame, conf=0.3)
    detections = results[0].boxes  # Get the boxes from YOLOv8 output

    for detection in detections:
        x1, y1, x2, y2 = map(int, detection.xyxy[0])  # Get bounding box coordinates
        conf = detection.conf.item()  # Confidence score
        class_id = int(detection.cls.item())  # Class index
        label = model.names[class_id]  # Get class name

        # If ROI is selected, only show objects inside the ROI
        if roi_selected:
            if (ref_point[0][0] <= x1 <= ref_point[1][0] and ref_point[0][1] <= y1 <= ref_point[1][1]):
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            # Draw detection on the entire frame if ROI isn't selected
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


# Open the video file or capture device
cap = cv2.VideoCapture('video_20240907_131754.avi')  # Replace with 0 for webcam

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Calculate the target frame rate to speed up the video
speed_up_factor = 5  # Speed up by 5x (5 min to 1 min)
new_fps = fps * speed_up_factor

# Calculate the frame skip factor
frame_skip = int(speed_up_factor)


cv2.namedWindow("Video")
cv2.setMouseCallback("Video", click_and_crop)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 object detection
    yolo_predict(frame)

    # Draw the selected ROI

    if roi_selected and len(ref_point) == 2:
        cv2.rectangle(frame, ref_point[0], ref_point[1], (0, 255, 0), 2)

    # Display the video frame
    cv2.imshow("Video", frame)
    cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + frame_skip)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):  # Press 'q' to quit the loop
        break

cap.release()
cv2.destroyAllWindows()