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
        print(int(heartbeat_interval)/1000)

        async def heart():
            data = {
                "op": 1,
                "d": None
            }
            data = json.dumps(data)

            await asyncio.sleep(int(heartbeat_interval)/1000)
            print("send")
            await websocket.send(data)
            await asyncio.create_task(heart())

        await heart()

asyncio.run(main())