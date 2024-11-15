import cv2
import numpy as np

# Load YOLOv8 model with custom weights

# Open the video capture (webcam or video file)
# cap = cv2.VideoCapture(0)  # Change '0' to the video file path if needed
cap = cv2.VideoCapture('video/video_20240913_171528.avi')
# Check if the video stream is opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Define a global variable to store clicked coordinates
clicked_coords = None

# Function to handle mouse click events
def click_event(event, x, y, flags, param):
    global clicked_coords
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_coords = (x, y)  # Store the clicked coordinates
        print(f"Clicked at: ({x}, {y})")

# Bind the mouse click event to the window
cv2.namedWindow('Video Stream')
cv2.setMouseCallback('Video Stream', click_event)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Perform YOLOv8 inference on the captured frame

    # Parse the results and draw bounding boxes on the frame


    # If coordinates were clicked, display them on the frame
    if clicked_coords:
        cv2.putText(frame, f'Clicked: {clicked_coords}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # Display the frame with detections and coordinates
    cv2.imshow('Video Stream', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
