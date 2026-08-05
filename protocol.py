import json

def create_chat_message(username:str, message:str):
    return {
        "type": "chat",
        "username": username,
        "message": message
    }
    
def create_join_message(username:str):
    return {
        "type": "join",
        "username": username,
        "message": f"📢 {username} joined the chat."
    }

def serialize(message: dict) -> str:
    return json.dumps(message)

def deserialize(message: str) -> dict:
    return json.loads(message)