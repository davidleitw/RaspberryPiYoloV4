from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware
from config import Config


if __name__ == '__main__':
    c = Config()
    app = FastAPI()
