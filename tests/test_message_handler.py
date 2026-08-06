import pytest
from unittest.mock import AsyncMock, MagicMock

from handlers.message_handler import MessageHandler
from models import ClientSession
from protocol import deserialize


@pytest.mark.anyio
async def test_message_handler_broadcasts_chat_message():
    manager = MagicMock()
    manager.broadcast = AsyncMock()

    handler = MessageHandler(manager)

    session = ClientSession(
        username="Alice",
        websocket=None,
    )

    await handler.handle_message(
        session,
        "Hello everyone!",
    )

    manager.broadcast.assert_awaited_once()

    args = manager.broadcast.await_args.args

    message = deserialize(args[0])

    assert message["type"] == "chat"
    assert message["username"] == "Alice"
    assert message["message"] == "Hello everyone!"
    
@pytest.mark.anyio
async def test_message_handler_routes_online_command():
    manager = MagicMock()
    manager.broadcast = AsyncMock()

    handler = MessageHandler(manager)

    session = ClientSession(
        username="Alice",
        websocket=None,
    )

    online_command = AsyncMock()
    handler.commands["online"] = online_command

    await handler.handle_message(
        session,
        "/online",
    )

    online_command.execute.assert_awaited_once_with(
        session,
        "",
    )

    manager.broadcast.assert_not_awaited()
    
@pytest.mark.anyio
async def test_message_handler_routes_private_message_command():
    manager = MagicMock()
    manager.broadcast = AsyncMock()

    handler = MessageHandler(manager)

    session = ClientSession(
        username="Alice",
        websocket=None,
    )

    private_command = AsyncMock()
    handler.commands["msg"] = private_command

    await handler.handle_message(
        session,
        "/msg Bob Hello Bob!",
    )

    private_command.execute.assert_awaited_once_with(
        session,
        "Bob Hello Bob!",
    )

    manager.broadcast.assert_not_awaited()
    
@pytest.mark.anyio
async def test_message_handler_returns_error_for_unknown_command():
    manager = MagicMock()
    manager.broadcast = AsyncMock()
    manager.send_to = AsyncMock()

    handler = MessageHandler(manager)

    session = ClientSession(
        username="Alice",
        websocket=None,
    )

    await handler.handle_message(
        session,
        "/unknown",
    )

    manager.broadcast.assert_not_awaited()

    manager.send_to.assert_awaited_once()

    args = manager.send_to.await_args.args

    assert args[0] == session

    message = deserialize(args[1])

    assert message["type"] == "error"
    assert message["message"] == "Unknown command: unknown"