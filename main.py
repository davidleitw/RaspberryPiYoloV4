from fastapi import FastAPI
from backend.detect import router
from yolov4.tf import YOLOv4

app = FastAPI()
app.include_router(router)

# yolo = YOLOv4()

# yolo.classes = "backend/coco.names"

# yolo.make_model()
# yolo.load_weights("backend/yolov4.weights", weights_type="yolo")

# yolo.inference(media_path="dog.jpg")
