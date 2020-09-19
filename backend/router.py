from fastapi import FastAPI
from fastapi import Depends, FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware
import detect as detect


app = FastAPI()

@app.get('/')
async def Hello():
    detect.detect()
    return {"Message": "Hello World"}

# import uvicorn
# if name == "main":
#    uvicorn.run(app,host="10.1.1.12",port=3000)