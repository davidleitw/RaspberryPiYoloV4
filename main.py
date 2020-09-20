from fastapi import FastAPI
from backend.detect import router
from yolov4.tf import YOLOv4
import uvicorn
import cv2

app = FastAPI()
app.include_router(router)

# if __name__ == '__main__':
#     uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True, debug=True)
