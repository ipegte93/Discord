import asyncio
import websockets

async def main():
    async with websockets.connect("wss://gateway.discord.gg") as websocket:
        data = await websocket.recv()
        print(data)

asyncio.run(main())