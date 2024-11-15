import cv2
from ultralytics import YOLO

# Load YOLOv8 model with custom weights
model = YOLO('weights/best_400.onnx')

# Open the video capture (webcam or camera feed)
# cap = cv2.VideoCapture('video_20240907_131754.avi')  # 0 is the default camera. Change it to the desired camera index if needed
cap = cv2.VideoCapture(0)


# Extract the ROI from the frame

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

x1, y1 = 0, 0
x2, y2 = 400, 400

while True:
    ret, frame = cap.read()


    if not ret:
        print("Error: Failed to capture frame.")
        break
    roi = frame[y1:y2, x1:x2]
    # Perform YOLOv8 inference on the captured frame
    results = model(frame)

    # Parse the results and draw bounding boxes on the frame
    for result in results:
        boxes = result.boxes.xyxy  # Bounding box coordinates (x1, y1, x2, y2)
        confidences = result.boxes.conf  # Confidence scores
        class_ids = result.boxes.cls  # Class IDs

        for box, conf, class_id in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)
            label = f'{model.names[int(class_id)]}: {conf:.2f}'

            # Draw bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with detections
    cv2.imshow('YOLOv8 Real-Time Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
