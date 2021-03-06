from fastapi import  WebSocket, APIRouter, UploadFile, File, status
from fastapi.responses import JSONResponse, HTMLResponse

import time
import numpy as np 
import cv2
from yolov4.tf import YOLOv4

router = APIRouter()

Yolo = YOLOv4()
Yolo.classes = 'backend/coco.names'
Yolo.make_model()
Yolo.load_weights("backend/yolov4.weights", weights_type="yolo")

@router.post('/yolov4')
async def yolov4_from_singleImage(files: UploadFile = File(...)):
    try: 
        file = await files.read()
        image = np.fromstring(file, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

        start = time.time()
        boxes = Yolo.predict(frame=image)
        result = Yolo.draw_bboxes(image, boxes)    
        end = time.time()
        
        print('time for detecting and draw boxes: {}'.format(end-start))
        cv2.imwrite(files.filename, result)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "result_image_size": "({}, {})".format(str(result.shape[0]), str(result.shape[1])),
                "image_size": "({}, {})".format(str(image.shape[0]), str(image.shape[1])),
                "image_name": files.filename,
                "run_time": str(end-start),
            }
        )
    except Exception as error:
        print("error = ", error)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": str(error),
            }
        )
    
