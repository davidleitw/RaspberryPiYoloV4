import cv2
import numpy as np 

from .detect import Yolo
from fastapi import  WebSocket, APIRouter, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse

socket_group = APIRouter()

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
            console.log(ws)
            ws.onmessage = function(frame) {
                console.log(frame.data)
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

class user(object):
    def __init__(self):
        user_id = 13

class websocketManager(object):
    def __init__(self):
        self.user_sockets: List[WebSocket] = []
        self.raspberry_socket: WebSocket = None
        self.raspberry_connection: bool = False
    
    async def raspberry_connect(self, ws: WebSocket):
        await ws.accept()
        self.raspberry_socket.append(ws)
        self.raspberry_connection = True
    
    async def user_connect(self, ws: WebSocket):
        await ws.accept()
        self.user_sockets.append(ws)

    async def raspberry_disconnect(self, ws: WebSocket):
        self.raspberry_socket = None
        self.raspberry_connection = False

    async def user_disconnect(self, ws: WebSocket):
        self.user_sockets.remove(ws)
    
    async def send_frame_broadcast(self, frame: bytes):
        for socket in self.user_sockets:
            await socket.send_bytes(frame)
    
    async def send_successful_msg(self):
        self.raspberry_socket.send_text("successfully sending image to frontend.")

manager = websocketManager()

@socket_group.get("/")
async def get():
    return HTMLResponse(html)

@socket_group.websocket('/ws/{user}')
async def websocket_connection(websocket: WebSocket, user: str):
    if user == 'frontend':
        manager.user_connect(websocket)
        try: 
            while manager.raspberry_connection:
                successfully_msg = await websocket.receive_str()
            else: # raspberrypi 斷線
                manager.user_disconnect(websocket)

        # manager.raspberry_connection is False, 代表目前raspberry沒有建立影像
        except WebSocketDisconnect:
            manager.user_disconnect(websocket)

    elif user == 'raspberry':
        manager.raspberry_connect(websocket)
        try:
            while True:
                data = await websocket.receive_bytes() # receive each frame data. 
                image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_UNCHANGED)

                boxes = Yolo.predict(frame=image) # input each frame to yolov4 model. 
                result_image = Yolo.draw_bboxes(image, boxes)

                # 廣播給所有跟backend連結的frontend
                manager.send_frame_broadcast(cv2.imencode(('.jpg', result_image)[1].tobytes()))
        
        except WebSocketDisconnect:
            manager.raspberry_disconnect()
