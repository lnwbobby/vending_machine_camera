import cv2

stream_url = "https://wework-5-us.stream.iot-11.com:8080/hls/ebd694af67ab160763w0ih/csbipplqmqsujpkamtfgiLjj5JJ93BfKnhx1vSHP.m3u8?signInfo=dy0WSz-oEo9z7NVg5EhN1tcCqHeLiRI6P37YHS4pyy81672GAIJeXExUggsRlrjyBgjG9K88xACjuB-8Br619nZ6X3WppYOMDAJeNDSP6EyYEVi8a0ckzise57tba7CQTeWQzKhlagq5XYTFs3l7IE4bxP-qOaTiOeA5zjnvLMw"

cap = cv2.VideoCapture(stream_url)


# Extract the ROI from the frame

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()


    if not ret:
        print("Error: Failed to capture frame.")
        break


    # Display the frame with detections
    cv2.imshow('YOLOv8 Real-Time Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
