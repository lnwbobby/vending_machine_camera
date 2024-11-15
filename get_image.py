import cv2

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use the appropriate camera index (0 is usually the default)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Capture a single frame
ret, frame = cap.read()

if ret:
    # Display the captured frame
    cv2.imshow('Empty Tray', frame)

    # Save the frame as an image file
    cv2.imwrite('empty_tray.jpg', frame)
    print("Empty tray image saved as 'empty_tray.jpg'.")

    # Wait for a key press to close the window
    cv2.waitKey(0)
else:
    print("Error: Could not capture image from camera.")

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
