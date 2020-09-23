import requests 

url = "http://127.0.0.1:8000/yolov4"

file = open('kite.jpg', 'rb')

# image = cv2.imread('dog.jpg')
files = {'files': file}
req = requests.post(url, files=files)
json = req.json()
print(json)
