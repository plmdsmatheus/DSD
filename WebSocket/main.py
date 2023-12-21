from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import socketio

app = FastAPI()
sio = socketio.AsyncServer(cors_allowed_origins="*")
app.add_middleware(socketio.ASGIMiddleware, sio)

@app.get("/")
async def get():
    return HTMLResponse(content=open("index.html").read())

@sio.event
async def connect(sid, environ):
    print(f"WebSocket connection opened for {sid}")

@sio.event
async def disconnect(sid):
    print(f"WebSocket connection closed for {sid}")

@sio.event
async def message(sid, data):
    await sio.send(sid, "Message from server: " + data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
