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
            receive_messages(websocket)
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
        
async def receive_messages(websocket):
    try:
        while True:
            print("Waiting for message...")
            response = await websocket.recv()
            protocol_message = deserialize(response)
            match protocol_message["type"]:
                case "chat":
                    print(f"\n{protocol_message['username']}: {protocol_message['message']}")
                case "join":
                    print(f"\n{protocol_message['message']}")
             
    except asyncio.CancelledError:
        print("Receiver task cancelled.")
        raise

    
        
if __name__ == "__main__":
    asyncio.run(main())