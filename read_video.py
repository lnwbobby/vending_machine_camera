import cv2

# Path to the recorded video
video_path = 'output.avi'  # or 'output.avi'

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
else:
    while True:
        # Read frame-by-frame
        ret, frame = cap.read()

        # If frame is read correctly, ret will be True
        if ret:
            # Display the frame
            cv2.imshow('Recorded Video', frame)

            # Press 'q' to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            print("End of video.")
            break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()