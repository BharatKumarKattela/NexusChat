

from connection_manager import ConnectionManager
from models import ClientSession


class MessageHandler:
    manager = ConnectionManager()
    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    async def handle_message(self, session: ClientSession, message: str):
        if message.startswith("/"):
            command = message.split(sep="/", maxsplit=1)
            if command[-1] == "online":
                count = self.manager.count()
                response = f"Active connections: {count}"
                await self.manager.send_to(session, response)
                return

        await self.manager.broadcast(f"{session.username}: {message}")