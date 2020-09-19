import os 
from dotenv import load_dotenv

class envReader(object):
    def __init__(self):
        load_dotenv()
    
    def getenv(self, key:str)->str:
        return os.getenv(key)

class Config(object):
    def __init__(self):
        self.reader = envReader()
        self.client_id = self.reader.getenv('client_id')
        self.client_secret = self.reader.getenv('client_secret')
        try:
            expire = int(self.reader.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
            self.expire_minutes = expire
        except ValueError:
            self.expire_minutes = 45
        self.yolo_cfg = {}
        self.yolo_cfg['model_def'] = "yolo/config/yolov3.cfg"
        self.yolo_cfg['img_size'] = 600
        self.yolo_cfg['weight_path'] = 'yolo/config/yolov3.weights'
        self.yolo_cfg['class_path'] = 'yolo/config/coco.names'

    def get_clientID(self)->str:
        return self.client_id
    def get_clientSecret(self)->str:
        return self.client_secret
    def get_expireMinutes(self)->int:
        return self.expire_minutes
    def get_yolocfg(self, key:str):
        return self.yolo_cfg.get(key, "Not found")

class Control(object):
    pass