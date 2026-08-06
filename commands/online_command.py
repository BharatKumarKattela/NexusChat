

from connection_manager import ConnectionManager
from models import ClientSession
from protocol import create_online_users_message, serialize


class OnlineCommand:
    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    async def execute(self, session: ClientSession, arguments: str = ""):
        users = self.manager.get_online_users()
        protocol_message = create_online_users_message(users)

        await self.manager.send_to(session, serialize(protocol_message))