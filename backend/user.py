from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, Body
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

class User(BaseModel):
    user_name: str
    user_email: str = None

async def login(
    username: str = Body(..., title='name'),
    password: str = Body(..., title='password'),
):
    return {"username": username, "password": password}
