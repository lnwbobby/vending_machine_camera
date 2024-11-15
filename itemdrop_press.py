import cv2
import numpy as np
import time
from collections import deque


# Function to calculate the difference between two frames in the ROI
def frame_difference(frame1, frame2, roi_pts):
    # Create masks for the ROI
    mask1 = np.zeros(frame1.shape[:2], dtype=np.uint8)
    mask2 = np.zeros(frame2.shape[:2], dtype=np.uint8)

    # Fill the ROI in the masks
    cv2.fillPoly(mask1, [roi_pts], 255)
    cv2.fillPoly(mask2, [roi_pts], 255)

    # Get the ROI for both frames using the mask
    roi_frame1 = cv2.bitwise_and(frame1, frame1, mask=mask1)
    roi_frame2 = cv2.bitwise_and(frame2, frame2, mask=mask2)

    # Compute the absolute difference
    diff = cv2.absdiff(roi_frame1, roi_frame2)

    # Convert the difference to grayscale
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Threshold to detect significant changes
    _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

    # Return the sum of the thresholded differences
    return np.sum(thresh)


# Define a deque to store the previous 5 seconds of frames
frame_buffer = deque(maxlen=150)  # Assuming 30 FPS, 5 seconds = 150 frames

# Define ROI points
pts = np.array([[470, 275],  # Bottom left
                [881, 245],  # Bottom right
                [870, 143],  # Top right
                [463, 168]], np.int32)  # Top left

# pts = np.array([[448, 259],  # Bottom left
#                 [851, 205],  # Bottom right
#                 [836, 102],  # Top right
#                 [431, 154]], np.int32)  # Top left

# Open video capture (0 for webcam or replace with your video stream)
# cap = cv2.VideoCapture(0)

init = 100

# cap = cv2.VideoCapture('video/video_20240918_093839.avi')
# start_time_seconds = 2000-init
# cap = cv2.VideoCapture('video/video_20240908_154312.avi')
# start_time_seconds = 1740-init
cap = cv2.VideoCapture('video/video_20240913_171528.avi')
start_time_seconds = 1200-init
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

print("Press 'c' to check for item drop...")

fps = cap.get(cv2.CAP_PROP_FPS)
# Loop to read and display the video

# Convert time to the equivalent frame number
start_frame = int(start_time_seconds * fps)
print(start_frame)
# Set the video to start at the calculated frame
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
# Default color for the ROI is green (no item drop)
roi_color = (255, 255, 255)
detecting = False
detect_time = 8  # Time in seconds for automatic detection
start_time = None  # Variable to track when detection started
first_frame = None  # To store the frame after pressing 'c'
start_video_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Store the frame in the buffer
    frame_buffer.append(frame)

    # Display the current frame with ROI
    cv2.polylines(frame, [pts], isClosed=True, color=roi_color, thickness=2)
    cv2.imshow("Frame", frame)


    key = cv2.waitKey(1) & 0xFF

    # If 'c' is pressed, start the detection
    if key == ord('c'):
        if len(frame_buffer) > 0:
            # Capture the frame after pressing 'c' as first_frame
            first_frame = frame_buffer[-1].copy()
            detecting = True
            start_time = time.time()
            print("Automatic detection started for 10 seconds...")

    if detecting == False:
        roi_color = (255, 255, 255)
    # Automatic detection for 10 seconds after pressing 'c'
    if detecting and start_time:
        if time.time() - start_time <= detect_time:
            if len(frame_buffer) > 1:
                # Compare the captured first frame with the latest frame in the buffer
                latest_frame = frame_buffer[-1]

                change = frame_difference(first_frame, latest_frame, pts)

                # If significant change is detected, change ROI color to red and print "item drop"
                print(change)
                # if change > 80000:
                if change > 1500000:  # Adjust this threshold based on your test

                    print("Item drop detected!",int(time.time()-start_video_time))
                    roi_color = (0, 0, 255)  # Red color for item drop
                else:
                    roi_color = (0, 255, 0)  # Green color if no item drop detected
        else:
            # Reset detecting state after 10 seconds
            detecting = False
            print("Automatic detection ended.")

    # Press 'q' to exit
    if key == ord('q'):
        break

# Release the capture and close any open windows
cap.release()
cv2.destroyAllWindows()
