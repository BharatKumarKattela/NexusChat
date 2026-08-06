import pytest
from models import ClientSession
from unittest.mock import AsyncMock

websocket = AsyncMock()

def test_count_returns_zero_for_new_manager(manager):
    result = manager.count()
    
    assert result == 0


def test_count_returns_number_of_active_sessions(manager, alice):
    manager.active_sessions.append(alice)
    assert manager.count() == 1
    
def test_get_session_returns_matching_session(manager, alice):
    manager.active_sessions.append(alice)
    
    result = manager.get_session("Alice")
    
    assert result == alice
    
def test_get_session_returns_none_when_username_does_not_exist(manager):
    result = manager.get_session("NonExistentUser")
    
    assert result is None


def test_username_exists_returns_true_for_existing_username(manager, alice):
    manager.active_sessions.append(alice)
    
    result = manager.username_exists("Alice")
    
    assert result is True
    
def test_username_exists_returns_false_for_nonexistent_username(manager):
    result = manager.username_exists("NonExistentUser")
    
    assert result is False
    
def test_get_online_users_returns_list_of_usernames(manager, alice, bob):
    manager.active_sessions.extend([alice, bob])
    
    result = manager.get_online_users()
    
    assert result == ["Alice", "Bob"]
    
def test_disconnect_removes_session(manager, alice):
    manager.active_sessions.append(alice)

    manager.disconnect(alice)
    assert manager.count() == 0
    
@pytest.mark.anyio
async def test_connect_accepts_websocket_and_adds_session(manager, alice):
    await manager.connect(alice)
    
    alice.websocket.accept.assert_awaited_once()

    assert manager.count() == 1
    
@pytest.mark.anyio
async def test_send_to_sends_message_to_session(manager, alice):
    await manager.send_to(alice, "Hello, Alice!")
    
    alice.websocket.send_text.assert_awaited_once_with("Hello, Alice!")
    
@pytest.mark.anyio
async def test_broadcast_sends_message_to_all_sessions(manager, alice, bob, charlie):
    
    manager.active_sessions.extend([alice, bob, charlie])
    
    await manager.broadcast("Hello, everyone!")
    
    alice.websocket.send_text.assert_awaited_once_with("Hello, everyone!")
    bob.websocket.send_text.assert_awaited_once_with("Hello, everyone!")
    charlie.websocket.send_text.assert_awaited_once_with("Hello, everyone!")
    
@pytest.mark.anyio
async def test_broadcast_except_sends_message_to_all_except_excluded_session(manager, alice, bob, charlie):
    
    manager.active_sessions.extend([alice, bob, charlie])
    
    await manager.broadcast_except("Hello, everyone!", exclude_session=bob)
    
    alice.websocket.send_text.assert_awaited_once_with("Hello, everyone!")
    bob.websocket.send_text.assert_not_awaited()
    charlie.websocket.send_text.assert_awaited_once_with("Hello, everyone!")