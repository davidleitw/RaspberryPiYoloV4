import requests
import cv2 
import os 
os.chdir('raspberryPI')

url = "http://127.0.0.1:8000/yolov4"
print(os.listdir())

file = open('dog.jpg', 'rb')
# image = cv2.imread('dog.jpg')
files = {'files': file}

req = requests.post(url, files=files)
print(req)