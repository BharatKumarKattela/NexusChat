

from connection_manager import ConnectionManager
from models import ClientSession
from commands.online_command import OnlineCommand
from protocol import create_chat_message, serialize

class MessageHandler:
    
    def __init__(self, manager: ConnectionManager):
        self.manager = manager
        self.commands = {
            "online": OnlineCommand(manager),
        }


    async def handle_message(self, session: ClientSession, message: str):
        if message.startswith("/"):
            command_name = message[1:].split(sep="/", maxsplit=1)
            command = self.commands.get(command_name[0].lower())
            if command:
                await command.execute(session)
                return
        protocol_message = create_chat_message(
            username=session.username,
            message=message
        )
        await self.manager.broadcast(serialize(protocol_message))