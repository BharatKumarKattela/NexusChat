from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager
from handlers.message_handler import MessageHandler
from models import ClientSession
app = FastAPI()
manager = ConnectionManager()
message_handler = MessageHandler(manager=manager)

@app.get("/")
async def health():
    return {
        "status": "Ok",
        "application": "NexusChat",
    }
    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str):
    
    if manager.username_exists(username):
        await websocket.accept()

        await websocket.send_text(
            f"ERROR: Username '{username}' is already in use."
        )

        await websocket.close()
        return
    
    session = ClientSession(username=username, websocket=websocket)
    await manager.connect(session)
    print("CLient connection established")
    await manager.broadcast_except(
        f"📢 {session.username} joined the chat.",
        exclude_session=session
        
    )
    print(f"Active connections: {manager.count()}")
    try:
        while True:
            message = await session.websocket.receive_text()    
            await message_handler.handle_message(
                session, 
                message
                )
    except WebSocketDisconnect:
        manager.disconnect(session)
        await manager.broadcast_except(
            f"📢 {session.username} left the chat.",
            exclude_session=session
        )
        print("Client connection closed")
        print(f"Active connections: {manager.count()}")