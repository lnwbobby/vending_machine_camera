import cv2
from ultralytics import YOLO
import numpy as np
# Load YOLOv8 model with custom weights
model = YOLO('weights/best_800.pt')

# Load the image instead of video capture
image_path = 'screen_shot/screenshot_20241002-201719.png'
frame = cv2.imread(image_path)

# Check if the image was loaded successfully
if frame is None:
    print("Error: Could not load image.")
    exit()


# height, width = frame.shape[:2]

# Define trapezoid points
# You can adjust these points to fit your trapezoid
pts = np.array([[440 , 259],  # Bottom left
                [426, 156],  # Bottom right
                [838, 105],  # Top right
                [853, 204]], np.int32)  # Top left

# Create a black mask
mask = np.zeros_like(frame)

# Fill the trapezoid area with white (255) on the mask
cv2.fillPoly(mask, [pts], (255, 255, 255))

# Apply the mask to the image to black out the outside of the trapezoid
masked_image = cv2.bitwise_and(frame, mask)

# Crop the region of interest (ROI) that contains the trapezoid
x, y, w, h = cv2.boundingRect(pts)  # Get bounding box around the trapezoid
cropped_image = masked_image[y:y + h, x:x + w]  # Crop the trapezoid area

# Resize the cropped image (scale up by 2)
scaled_image = cv2.resize(cropped_image, (w * 2, h * 2), interpolation=cv2.INTER_LINEAR)
# Display the scaled-up ROI
# cv2.imshow('Scaled ROI', scaled_image)

# Perform YOLOv8 inference on the original frame (if needed)
results = model(scaled_image, conf=0.2)

# Parse the results and draw bounding boxes on the original masked image (if needed)
for result in results:
    boxes = result.boxes.xyxy  # Bounding box coordinates (x1, y1, x2, y2)
    confidences = result.boxes.conf  # Confidence scores
    class_ids = result.boxes.cls  # Class IDs

    for box, conf, class_id in zip(boxes, confidences, class_ids):
        x1, y1, x2, y2 = map(int, box)
        label = f'{model.names[int(class_id)]}: {conf:.2f}'

        # Draw bounding box and label on the masked image
        cv2.rectangle(scaled_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(scaled_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the image with detections and masked outside the trapezoid
cv2.imshow('YOLOv8 Detection with Trapezoid Mask', scaled_image)

# Wait for a key press and close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()