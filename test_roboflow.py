from inference import get_model
import supervision as sv
import cv2

# define the image url to use for inference
image_file = "taylor-swift-album-1989.jpeg"
image = cv2.imread(image_file)

# load a pre-trained yolov8n model
model = get_model(model_id="taylor-swift-records/3")