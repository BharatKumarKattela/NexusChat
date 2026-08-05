

import asyncio

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: list[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    def count(self):
        return len(self.active_connections)
        
    async def broadcast(self, message: str):
        print("=" * 50)
        print(f"Broadcasting: {message}")
        print(f"Active connections: {len(self.active_connections)}")
        
        tasks = []

        for index, connection in enumerate(self.active_connections, start=1):
            print(f"Scheduled send to connection #{index}")

            # await connection.send_text(message)
            task = asyncio.create_task(connection.send_text(message))
            tasks.append(task)
            print(f"Finished sending to connection #{index}")
        await asyncio.gather(*tasks, return_exceptions=True)  # Optional: Add a small delay between sends
        print("Broadcast completed.")
        print("=" * 50)