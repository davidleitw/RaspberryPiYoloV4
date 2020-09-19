from fastapi import  WebSocket, APIRouter
from fastapi.responses import HTMLResponse

import numpy as np 
import cv2
from yolov4.tf import YOLOv4

router = APIRouter()

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
          
        data = yolo.predict(frame=image)
        result = yolo.draw_bboxes(image, data)
        cv2.imshow('frame', result)
        await websocket.send_text("keep connection")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

