from fastapi import  WebSocket, APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse

import time
import numpy as np 
import cv2
from yolov4.tf import YOLOv4

class yolo(object):
    def __init__(self):
        self.yolo = YOLOv4()
        self.yolo.classes = 'backend/coco.names'
        self.yolo.make_model()
        self.yolo.load_weights("backend/yolov4.weights", weights_type="yolo")

router = APIRouter()
Yolo = yolo()

@router.get('/')
async def hello():
    return {"msg": "Hello world"}

@router.websocket('/ws')
async def websocket_connection(websocket: WebSocket):
    await websocket.accept()
    yolo = YOLOv4()
    yolo.classes = 'coco.names'
    yolo.make_model()
    yolo.load_weights("yolov4.weights", weights_type="yolo")

    while True:
        _frame = await websocket.receive_bytes()
        nparray = np.frombuffer(_frame, np.uint8)
        image = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
          
        boxes = yolo.predict(frame=image)
        result = yolo.draw_bboxes(image, boxes)
        cv2.imshow('frame', result)
        await websocket.send_text("keep connection")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

@router.post('/yolov4')
async def yolov4_from_singleImage(files: UploadFile = File(...)):
    try: 
        file = await files.read()
        image = np.fromstring(file, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

        boxes = Yolo.yolo.predict(frame=image)
        result = Yolo.yolo.draw_bboxes(image, boxes)    
        cv2.imshow('image', result)
        cv2.waitKey(0)
        time.sleep(10)
        cv2.destroyAllWindows()   
        return {"message": "got your image, and show the image on the server"}
    except Exception as e:
        print("error = ", e)
        return {"message": str(e)}
    