from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager
app = FastAPI()
manager = ConnectionManager()


@app.get("/")
async def health():
    return {
        "status": "Ok",
        "application": "NexusChat",
    }
    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print("CLient connection established")
    print(f"Active connections: {manager.count()}")
    try:
        while True:
            message = await websocket.receive_text()    
            print(f"Received from client: {message}")     
            await manager.broadcast(f"Message received: {message}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client connection closed")
        print(f"Active connections: {manager.count()}")