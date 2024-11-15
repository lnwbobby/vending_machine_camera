import cv2
import time

# Open video file
cap = cv2.VideoCapture('video/video_20240918_093839.avi')

# Check if video opened successfully
if not cap.isOpened():
    print("Error opening video file")

# Set a counter for screenshots

fps = cap.get(cv2.CAP_PROP_FPS)
# Loop to read and display the video
start_time_seconds = 2040
# Convert time to the equivalent frame number
start_frame = int(start_time_seconds * fps)

# Set the video to start at the calculated frame
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
screenshot_counter = 0
while cap.isOpened():
    ret, frame = cap.read()

    # Break the loop if no frame is captured (end of video)
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the frame
    cv2.imshow('Video', frame)

    # Capture key press
    key = cv2.waitKey(1) & 0xFF

    # If 's' key is pressed, save a screenshot
    if key == ord('s'):
        screenshot_counter += 1
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f'screenshot_{timestamp}.png'
        cv2.imwrite('screen_shot/'+filename, frame)
        print(f"Screenshot saved as {filename}")

    # Break the loop if 'q' key is pressed
    if key == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
