from fastapi import  WebSocket, APIRouter, UploadFile, File, status
from fastapi.responses import JSONResponse, HTMLResponse

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

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://10.1.1.12:3000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket('/ws')
async def websocket_connection(websocket: WebSocket):
    await websocket.accept()

    while True:
        _frame = await websocket.receive_bytes()
        nparray = np.frombuffer(_frame, np.uint8)
        image = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
          
        boxes = Yolo.yolo.predict(frame=image)
        result = Yolo.yolo.draw_bboxes(image, boxes)
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
        print(
            "filename = ", files.filename, "\n",
            "boxes => ({}): {}\n".format(
                boxes.shape,
                boxes,
            )
        )
        result = Yolo.yolo.draw_bboxes(image, boxes)    
        cv2.imwrite(files.filename, result)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "result_image_size": "({}, {})".format(str(result.shape[0]), str(result.shape[1])),
                "image_size": "({}, {})".format(str(image.shape[0]), str(image.shape[1])),
                "image_name": files.filename,
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
    