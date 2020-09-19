from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, Body, Request
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

class User(BaseModel):
    user_name: str
    user_email: str = None

class Oauth2(object):
    def __init__(self):
        self.config = Config('.env')
        self.oauth = OAuth(self.config)
        self.oauth.register(
            name='google',
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile',
            }    
        )

    async def login(self, request: Request):
        redirect_uri = request.url_for('callback')
        return await self.ouath.google.authorize_redirect(request, redirect_uri)

    async def callback(self, request: Request):
        access_token = await self.ouath.google.authorize_access_token(request)
        user = await self.oauth.google.parse_id_token(request, access_token)
        return user