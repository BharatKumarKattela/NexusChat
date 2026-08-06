from commands.online_command import OnlineCommand
from unittest.mock import AsyncMock, MagicMock
import pytest
from commands.private_message_command import PrivateMessageCommand
from models import ClientSession
from protocol import deserialize, serialize

@pytest.mark.anyio
async def test_online_command_execution():
    manager = MagicMock()
    manager.get_online_users.return_value = ["Alice", "Bob"]
    command = OnlineCommand(manager)
    session = ClientSession(
        username="Charlie",
        websocket=None
    )
    
    manager.send_to = AsyncMock()
    
    await command.execute(session)
    manager.get_online_users.assert_called_once()
    manager.send_to.assert_awaited_once()
    args = manager.send_to.await_args.args
    assert args[0] == session

    message = deserialize(args[1])

    assert message["type"] == "online_users"
    assert message["users"] == ["Alice", "Bob"]
    
@pytest.mark.anyio
async def test_online_command_sends_empty_online_users_list():
    manager = MagicMock()
    manager.get_online_users.return_value = []
    command = OnlineCommand(manager)
    session = ClientSession(
        username="Charlie",
        websocket=None
    )
    
    manager.send_to = AsyncMock()
    
    await command.execute(session)
    manager.get_online_users.assert_called_once()
    manager.send_to.assert_awaited_once()
    args = manager.send_to.await_args.args
    assert args[0] == session

    message = deserialize(args[1])

    assert message["type"] == "online_users"
    assert message["users"] == []
    
@pytest.mark.anyio
async def test_private_message_command_sends_message_to_recipient_and_sender():
    manager = MagicMock()
    
    sender = ClientSession(username="Alice", websocket=None)
    recipient = ClientSession(username="Bob", websocket=None)
    
    manager.get_session.return_value = recipient
    manager.send_to = AsyncMock()
    
    command = PrivateMessageCommand(manager)
    await command.execute(sender, "Bob Hello, Bob!")
    manager.get_session.assert_called_once_with("Bob")
    assert manager.send_to.await_count == 2
    calls = manager.send_to.await_args_list
    
    assert calls[0].args[0] == recipient
    recipient_message = deserialize(calls[0].args[1])
    
    assert recipient_message["type"] == "private"
    assert recipient_message["sender"] == "Alice"
    assert recipient_message["recipient"] == "Bob"
    assert recipient_message["message"] == "Hello, Bob!"
    
    
    assert calls[1].args[0] == sender
    sender_message = deserialize(calls[1].args[1])
    
    assert sender_message == recipient_message
    
@pytest.mark.anyio
async def test_private_message_command_returns_error_when_user_is_not_online():
    manager = MagicMock()

    manager.get_session.return_value = None
    manager.send_to = AsyncMock()

    sender = ClientSession(
        username="Alice",
        websocket=None,
    )

    command = PrivateMessageCommand(manager)

    await command.execute(
        sender,
        "Bob Hello",
    )

    manager.get_session.assert_called_once_with("Bob")

    manager.send_to.assert_awaited_once()

    args = manager.send_to.await_args.args

    assert args[0] == sender

    message = deserialize(args[1])

    assert message["type"] == "error"
    assert message["message"] == "User 'Bob' is not online."
    
@pytest.mark.anyio
async def test_private_message_command_returns_usage_when_arguments_are_invalid():
    manager = MagicMock()

    manager.send_to = AsyncMock()

    sender = ClientSession(
        username="Alice",
        websocket=None,
    )

    command = PrivateMessageCommand(manager)

    await command.execute(
        sender,
        "Bob",
    )

    manager.get_session.assert_not_called()

    manager.send_to.assert_awaited_once()

    args = manager.send_to.await_args.args

    assert args[0] == sender

    message = deserialize(args[1])

    assert message["type"] == "error"
    assert message["message"] == "Usage: /msg <username> <message>"