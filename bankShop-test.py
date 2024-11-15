from ultralytics import YOLO
import os
import cv2
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
model = YOLO("weights/best_400.onnx")  # load a pretrained model (recommended for training)
# results = model.predict("messageImage_1724776377499.jpg",save=True)  # predict on an image
# path = model.export(format="onnx")  # export the model to ONNX format
username = "admin"
password = "P@ssw0rd"
camera_ip = "192.168.1.108"
port = 554
channel = 1
subtype = 0

# Construct the RTSP URL
# rtsp_url = f"rtsp://{username}:{password}@{camera_ip}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}"


cap = cv2.VideoCapture(0)
#
# if not cap.isOpened():
#     print("Error: Cannot open the RTSP stream")
#     exit()
#
# while True:
#     # Capture frame-by-frame from the stream
#     ret, frame = cap.read()
#
#     if not ret:
#         print("Error: Cannot read the frame")
#         break
#
#     # Resize the frame to 640x640 before prediction
#     frame_resized = cv2.resize(frame, (640, 640))
#
#     # Perform YOLOv8 prediction on the resized frame
#     results = model.predict(frame_resized, conf=0.7, iou=0.9)
#
#     # Draw bounding boxes on the resized frame
#     for r in results:
#         # Access the bounding boxes
#         boxes = r.boxes
#         for box in boxes.xyxy:  # xyxy format
#             x1, y1, x2, y2 = map(int, box)
#             # Draw a rectangle around the detected object
#             cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
#
#     # Display the resized frame with bounding boxes
#     cv2.imshow('Resized Stream with Bounding Boxes', frame_resized)
#
#     # Press 'q' to exit the stream
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Release resources and close windows
# cap.release()
# cv2.destroyAllWindows()

results = model.predict(0,show=True, conf=0.7, iou = 0.5)  # predict on an cam
# # Process results generator
# for result in results:
#     boxes = result.boxes  # Boxes object for bounding box outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     obb = result.obb  # Oriented boxes object for OBB outputs
#     result.show()  # display to screen
#     # result.save(filename="result.jpg")  # save to disk
#     print(obb)
