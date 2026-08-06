import asyncio
from websockets.asyncio.client import connect

from protocol import deserialize

async def main():
    print("Connecting to NexusChat...")
    username = input("Username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    async with connect(f"ws://127.0.0.1:8000/ws?username={username}") as websocket:
        print("Connected to NexusChat!")
        sender = asyncio.create_task(
            send_messages(websocket)
        )

        receiver = asyncio.create_task(
            receive_messages(websocket, username)
        )
        await sender
        receiver.cancel()  # Cancel the receiver task when sender is done
        try:
            await receiver  # Await the receiver to handle cancellation properly
        except asyncio.CancelledError:
            print("Receiver task has been cancelled.")
            
            
async def send_messages(websocket):
    while True:
        message = await asyncio.to_thread(input, "> ")
        if message.lower() == "exit":
            print("Exiting...")
            break
        await websocket.send(message)
        
async def receive_messages(websocket, username: str):
    try:
        while True:
            print("Waiting for message...")
            received_message  = await websocket.recv()
            protocol_message = deserialize(received_message )
            match protocol_message["type"]:
                case "private":
                    if protocol_message["sender"] == username:
                        print(
                            f"\n[You → {protocol_message['recipient']}] "
                            f"{protocol_message['message']}"
                        )
                    else:
                        print(
                            f"\n[Private] {protocol_message['sender']}: "
                            f"{protocol_message['message']}"
                        )
                case "error":
                    print(f"\n❌ {protocol_message['message']}")
                case "chat":
                    print(f"\n{protocol_message['username']}: {protocol_message['message']}")
                case "join":
                    print(f"\n{protocol_message['message']}")
                case "leave":
                    print(f"\n{protocol_message['message']}")
                case "online_users":
                    print(
                        "\nOnline Users:\n"
                        + "\n".join(
                            f"• {user}"
                            for user in protocol_message["users"]
                        )
                    )
                case _:
                    print(f"\nUnknown protocol message: {protocol_message}")
             
    except asyncio.CancelledError:
        print("Receiver task cancelled.")
        raise

    
        
if __name__ == "__main__":
    asyncio.run(main())