from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager
from handlers.message_handler import MessageHandler
from models import ClientSession
from protocol import create_error_message, create_join_message, create_leave_message, serialize
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
            serialize(
                create_error_message(
                    f"Username '{username}' is already taken."
                )
            )
        )

        await websocket.close()
        return
    
    session = ClientSession(username=username, websocket=websocket)
    await manager.connect(session)
    print("CLient connection established")
    join_message = create_join_message(username)
    await manager.broadcast_except(
        serialize(join_message),
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
        leave_message = create_leave_message(username)
        await manager.broadcast_except(
            serialize(leave_message),
            exclude_session=session
        )
        print("Client connection closed")
        print(f"Active connections: {manager.count()}")