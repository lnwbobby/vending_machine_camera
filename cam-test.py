import cv2

# Open the video file
cap = cv2.VideoCapture('video_20240907_131754.avi')

# Get the original frame rate of the video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Calculate the target frame rate to speed up the video
speed_up_factor = 5  # Speed up by 5x (5 min to 1 min)
new_fps = fps * speed_up_factor

# Calculate the frame skip factor
frame_skip = int(speed_up_factor)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Display the frame
    cv2.imshow('Video Speed-Up', frame)

    # Skip frames to achieve the desired speed
    cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + frame_skip)

    # Adjust the playback delay according to the new FPS
    # if cv2.waitKey(int(1000 // new_fps)) & 0xFF == ord('q'):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
