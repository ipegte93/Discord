import asyncio
import websockets
import json

#TODO identify 과정 추가

class Websocket:
    async def connect(self):
        async with websockets.connect("wss://gateway.discord.gg") as self.ws:
            await self.handler()

    async def handler(self):
        while True:
            msg = await self.ws.recv()
            msg = json.loads(msg)
            print(msg)
            await self.consumer(msg)

    async def consumer(self, msg):
        op = msg["op"]
        if op == 0: # Dispatch
            print(msg)
        if op == 7: # Reconnect
            print(msg)
        if op == 9: # Invalid Session
            print(msg)
        if op == 10: # Hello
            self.interval = int(msg["d"]["heartbeat_interval"])/1000
            asyncio.create_task(self.heartbeat())
        if op == 11: #Heartbeat ACK
            asyncio.create_task(self.heartbeat())

    async def heartbeat(self):
        await asyncio.sleep(self.interval)

        data = {
            "op": 1,
            "d": None
        }
        data = json.dumps(data)

        print("send Heartbeat")
        await self.ws.send(data)

if __name__ == "__main__":
    test = Websocket()
    asyncio.run(test.connect())