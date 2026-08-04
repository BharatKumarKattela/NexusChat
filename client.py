import asyncio
from websockets.asyncio.client import connect

async def main():
    print("Connecting to NexusChat...")

    async with connect("ws://127.0.0.1:8000/ws") as websocket:
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
            response = await websocket.recv()
            print(f"Received from server: {response}")  
    except asyncio.CancelledError:
        print("Receiver task cancelled.")
        raise

    
        
if __name__ == "__main__":
    asyncio.run(main())