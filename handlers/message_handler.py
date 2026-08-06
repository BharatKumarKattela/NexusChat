

from commands.private_message_command import PrivateMessageCommand
from connection_manager import ConnectionManager
from models import ClientSession
from commands.online_command import OnlineCommand
from protocol import create_chat_message, serialize

class MessageHandler:
    
    def __init__(self, manager: ConnectionManager):
        self.manager = manager
        self.commands = {
            "online": OnlineCommand(manager),
            "msg": PrivateMessageCommand(manager)
        }


    async def handle_message(self, session: ClientSession, message: str):
        if message.startswith("/"):
            parts = message[1:].split(maxsplit=1)
            command_name = parts[0].lower()
            arguments = parts[1] if len(parts) > 1 else ""
            command = self.commands.get(command_name)
            if command:
                await command.execute(session, arguments)
                return
        
        protocol_message = create_chat_message(
            username=session.username,
            message=message
        )
        await self.manager.broadcast(serialize(protocol_message))