from operator import mod

import torch 
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch.autograd import Variable

from yolo.models import Darknet
from yolo.utils.utils import * 
from yolo.utils.datasets import *
from conf import Config

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

import numpy as np 
import cv2
from PIL import Image


# config obj
config = Config()

# define device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# set up model
model = Darknet(config.get_yolocfg('model_def'), img_size=config.get_yolocfg('img_size')).to(device)
model.load_darknet_weights(config.get_yolocfg('weight_path'))
model.eval()

classes = load_classes(config.get_yolocfg('class_path'))
Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

loader = transforms.Compose(
    [
        transforms.Resize(416),
        transforms.ToTensor(),
    ]
)

async def websocket_connection(websocket: WebSocket):
    await websocket.accept()
    while True:
        frame = await websocket.receive_bytes()
        nparray = np.frombuffer(frame, np.uint8)
        source_image = image
        image = cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)
        source_image = image

        image = loader(image).float()
        image = Variable(image, require_grad=True)

        with torch.no_grad():
            detections = model(image)
            detections = non_max_suppression(detections, 0.8, 0.4)

        print(type(detections))
        print(source_image)            
        await websocket.send_text("keep connection")

