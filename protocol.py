import json
from typing import Any

ProtocolMessage = dict[str, Any]
def create_chat_message(username:str, message:str)->ProtocolMessage:
    return {
        "type": "chat",
        "username": username,
        "message": message
    }
    
def create_join_message(username:str)-> ProtocolMessage:
    return {
        "type": "join",
        "username": username,
        "message": f"📢 {username} joined the chat."
    }
    
def create_leave_message(username: str)-> ProtocolMessage:
    return {
            "type": "leave",
            "username": username,
            "message": f"📢 {username} left the chat."
        }
 
def create_error_message(message: str) -> ProtocolMessage:
    return {
        "type": "error",
        "message": message,
    }

def create_online_users_message(users: list[str]) -> ProtocolMessage:
    return {
        "type": "online_users",
        "users": users
    }
    
def create_private_message(sender: str, recipient: str, message: str) -> ProtocolMessage:
    return {
        "type": "private",
        "sender": sender,
        "recipient": recipient,
        "message": message,
    }

def serialize(message: ProtocolMessage) -> str:
    return json.dumps(message)

def deserialize(message: str) -> ProtocolMessage:
    return json.loads(message)