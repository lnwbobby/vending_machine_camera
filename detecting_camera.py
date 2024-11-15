import cv2
import numpy as np
import time
from collections import deque

# Function to calculate frame difference in the specified ROI
def frame_difference(frame1, frame2, roi_pts):
    mask1 = np.zeros(frame1.shape[:2], dtype=np.uint8)
    mask2 = np.zeros(frame2.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask1, [roi_pts], 255)
    cv2.fillPoly(mask2, [roi_pts], 255)
    roi_frame1 = cv2.bitwise_and(frame1, frame1, mask=mask1)
    roi_frame2 = cv2.bitwise_and(frame2, frame2, mask=mask2)
    diff = cv2.absdiff(roi_frame1, roi_frame2)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
    return np.sum(thresh)

# Function to set up video capture and seek to start frame
def setup_video_capture(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return None
    return cap

# Function to perform item drop detection within the detection time
def detect_item_drop(cap, frame_buffer, roi_pts, detect_time, threshold,detect_frame):
    start_time = time.time()
    detecting = True
    count_detection = 0

    # Ensure at least one frame in the buffer before starting detection
    while len(frame_buffer) == 0:
        ret, frame = cap.read()
        if not ret:
            print("Error: No frames to read.")
            return
        frame_buffer.append(frame)

    # Capture the first frame for reference
    first_frame = frame_buffer[-1].copy()
    print("Automatic detection started for 10 seconds...")

    while detecting:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Frame", frame)
        frame_buffer.append(frame)

        if len(frame_buffer) > 1:
            latest_frame = frame_buffer[-1]
            change = frame_difference(first_frame, latest_frame, roi_pts)
            print("Change value:", change)

            if change > threshold:

                count_detection += 1
                print("Item drop detected : ", count_detection)
            # else:
            #     print("No item drop detected.")
            if count_detection >= detect_frame:
                detecting = False
                print("Item drop detected!!!!")
                cap.release()
                return True
        if time.time() - start_time > detect_time:
            print("Detection time ended.")
            detecting = False
            cap.release()
            return False

# Main function to initialize parameters and start detection
def main():
    video_path = 0
    # username = "admin"
    # password = "P@ssw0rd"
    # camera_ip = "192.168.1.108"
    # port = "554"
    # channel = "1"
    # subtype = "0"
    # rtsp_url = f"rtsp://{username}:{password}@{camera_ip}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}"
    start_time_seconds = 1200  # Define your start time here
    fps_offset = 100
    roi_pts = np.array([[470, 275], [881, 245], [870, 143], [463, 168]], np.int32)
    frame_buffer = deque(maxlen=150)

    cap = setup_video_capture(video_path)
    if not cap:
        return

    print("Starting automatic detection for 10 seconds...")
    status = detect_item_drop(cap, frame_buffer, roi_pts,detect_time=10,threshold=1500000,detect_frame=30)
    print(status)


if __name__ == "__main__":
    main()
