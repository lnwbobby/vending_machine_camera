import cv2
import time
import os

# Open the RTSP stream using OpenCV
username = "admin"
password = "P@ssw0rd"
camera_ip = "192.168.1.108"
port = "554"
channel = "1"
subtype = "0"
rtsp_url = f"rtsp://{username}:{password}@{camera_ip}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}"

cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Cannot open the RTSP stream")
    exit()

# Get the video frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up the video writer with a timestamp filename
timestamp = time.strftime("%Y%m%d_%H%M%S")
filename = f"video_{timestamp}.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(filename, fourcc, 20.0, (frame_width, frame_height))

print(f"Recording video to {filename}")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Cannot read the frame")
        break

    # Write the frame to the video file
    out.write(frame)

    # Display the frame (optional)
    cv2.imshow('Recording Video', frame)

    # Press 'q' to exit the video recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Video recording finished. Saved as {filename}")