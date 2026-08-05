

import asyncio

from fastapi import WebSocket

from models import ClientSession


class ConnectionManager:

    def __init__(self):
        self.active_sessions: list[ClientSession] = []
            
    async def connect(self, session: ClientSession):
        await session.websocket.accept()
        self.active_sessions.append(session)
        
    def disconnect(self, session: ClientSession):
        self.active_sessions.remove(session)
        
    
    def count(self):
        return len(self.active_sessions)
        
    async def broadcast(self, message: str):
        print("=" * 50)
        print(f"Broadcasting: {message}")
        print(f"Active connections: {len(self.active_sessions)}")
        
        tasks = []

        for index, session in enumerate(self.active_sessions, start=1):
            print(f"Scheduled send to connection #{index}")
            task = asyncio.create_task(session.websocket.send_text(message))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)  # Optional: Add a small delay between sends
        print("Broadcast completed.")
        print("=" * 50)
        
    async def broadcast_except(self, message: str, exclude_session: ClientSession | None = None):
        print("=" * 50)
        print(f"Broadcasting: {message}")
        print(f"Active connections: {len(self.active_sessions)}")
        
        tasks = []

        for index, session in enumerate(self.active_sessions, start=1):
            if exclude_session == session:
                continue
            print(f"Scheduled send to connection #{index}")
            task = asyncio.create_task(session.websocket.send_text(message))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)  # Optional: Add a small delay between sends
        print("Broadcast completed.")
        print("=" * 50)
        
    def username_exists(self, username: str) -> bool:
        return any(session.username == username for session in self.active_sessions)
    
    async def send_to(self, session: ClientSession, message: str):
        await session.websocket.send_text(message)
        
    def get_online_users(self) -> list[str]:
        return [session.username for session in self.active_sessions]