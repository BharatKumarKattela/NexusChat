from unittest.mock import AsyncMock

import pytest

from connection_manager import ConnectionManager
from models import ClientSession


@pytest.fixture
def manager():
    return ConnectionManager()

@pytest.fixture
def websocket():
    return AsyncMock()


@pytest.fixture
def alice():
    return ClientSession(
        username="Alice",
        websocket=AsyncMock(),
    )


@pytest.fixture
def bob():
    return ClientSession(
        username="Bob",
        websocket=AsyncMock(),
    )


@pytest.fixture
def charlie():
    return ClientSession(
        username="Charlie",
        websocket=AsyncMock(),
    )