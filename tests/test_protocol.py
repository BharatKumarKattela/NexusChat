from protocol import  (
    create_error_message, 
    create_leave_message, 
    create_join_message,
    create_online_users_message, 
    serialize, 
    deserialize, 
    create_private_message, 
    create_chat_message
)

def test_online_users_message():
    users = ["Alice", "Bob", "Charlie"]
    result = create_online_users_message(users)
    assert result["type"] == "online_users"
    assert result["users"] == users

def test_create_chat_message():
    username = "Bharat"
    message = "Hello, World!"
    result = create_chat_message(username, message)
    assert result["type"] == "chat"
    assert result["username"] == username
    assert result["message"] == message

def test_create_private_message():
    sender = "Alice"
    recipient = "Bob"
    message = "Hello, Bob!"
    result = create_private_message(sender, recipient, message)
    assert result["type"] == "private"
    assert result["sender"] == sender
    assert result["recipient"] == recipient
    assert result["message"] == message

def test_create_error_message():
    error_text = "An error occurred."
    result = create_error_message(error_text)
    assert result["type"] == "error"
    assert result["message"] == error_text

def test_create_join_messages():
    username = "Bharat"
    result = create_join_message(username)
    assert result["type"] == "join"
    assert result["username"] == username
    assert result["message"] == f"📢 {username} joined the chat."

def test_create_leave_messages():
    username = "Bharat"
    result = create_leave_message(username)
    assert result["type"] == "leave"
    assert result["username"] == username
    assert result["message"] == f"📢 {username} left the chat."


def test_serialize_deserialize():
    original_message = {
        "type": "chat",
        "username": "Bharat",
        "message": "Hello, World!"
    }
    serialized_message = serialize(original_message)
    deserialized_message = deserialize(serialized_message)
    assert deserialized_message == original_message
    
def test_serialize_deserialize_private_message():
    original_message = {
        "type": "private",
        "sender": "Alice",
        "recipient": "Bob",
        "message": "Hello, Bob!"
    }
    serialized_message = serialize(original_message)
    deserialized_message = deserialize(serialized_message)
    assert deserialized_message == original_message