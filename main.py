from yolov4.tf import YOLOv4
import cv2

yolo = YOLOv4()

yolo.classes = "backend/yolo/config/coco.names"

yolo.make_model()
yolo.load_weights("yolov4.weights", weights_type="yolo")

yolo.inference(media_path="dog.jpg")

# frame = cv2.imread("dog.jpg")
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# bboxes = predict(
#                 frame,
#                 iou_threshold=0.3,
#                 score_threshold=0.25,
#             )

# frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
# image = draw_bboxes(frame, bboxes)