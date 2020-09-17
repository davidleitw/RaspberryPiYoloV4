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
        self.client_id = self.reader.getenv('CLIENT_ID')
        self.client_secret = self.reader.getenv('CLIENT_SECRET')
        try:
            expire = int(self.reader.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
            self.expire_minutes = expire
        except ValueError:
            self.expire_minutes = 45
        self.session_key = self.reader.getenv('SESSION_KEY')
        
    def get_clientID(self)->str:
        return self.client_id
    def get_clientSecret(self)->str:
        return self.client_secret
    def get_expireMinutes(self)->int:
        return self.expire_minutes
    def get_sessionKey(self)->str:
        return self.session_key
