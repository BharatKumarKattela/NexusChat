from dataclasses import dataclass
from fastapi import WebSocket

@dataclass
class ClientSession:
    username: str
    websocket: WebSocket