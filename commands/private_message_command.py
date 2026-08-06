

from connection_manager import ConnectionManager
from models import ClientSession
from protocol import create_private_message, serialize


class PrivateMessageCommand:
    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    async def execute(self, session: ClientSession, arguments: str = ""):
        print(f"Executing private message command with arguments: {arguments}")
        parts = arguments.split(maxsplit=1)
        if len(parts) < 2:
            await self.manager.send_to(session, "Usage: /msg <username> <message>")
            return
        recipient_username, message = parts
        recipient_session = self.manager.get_session(recipient_username)
        if not recipient_session:
            await self.manager.send_to(session, f"User '{recipient_username}' is not online.")
            return
        
        private_message = create_private_message(session.username, recipient_username, message)
        await self.manager.send_to(recipient_session, serialize(private_message))
        await self.manager.send_to(session, serialize(private_message))