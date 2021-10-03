import asyncio
import websockets
import json

async def heartbeat(interval):

    data = {
    "op": 1,
    "d" : None
    }
    print(interval)
    await asyncio.sleep(int(interval)/1000)
    return json.dumps(data)

async def main():
    async with websockets.connect("wss://gateway.discord.gg") as websocket:
        res = await websocket.recv()
        res = json.loads(res)

        heartbeat_interval = res["d"]["heartbeat_interval"]
        data = await heartbeat(heartbeat_interval)
        await websocket.send(data)

asyncio.run(main())