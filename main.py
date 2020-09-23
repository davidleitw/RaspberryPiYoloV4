from fastapi import FastAPI
from backend.detect import router
from backend.websocket import socket_group

app = FastAPI()
app.include_router(router)
app.include_router(socket_group)

# if __name__ == '__main__':
#     uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True, debug=True)
