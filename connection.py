import asyncio
import websockets
import json
import sys
import aiohttp

class Websocket:
    def __init__(self, BOT_TOKEN: str):
        self.TOKEN = BOT_TOKEN

    def start(self):
        asyncio.run(self.connect())

    async def connect(self):
        async with websockets.connect("wss://gateway.discord.gg") as self.ws:
            await self.handler()

    async def identify(self):
        data = {
            "op": 2,
            'd': {
                "token": self.TOKEN,
                "intents": 513,
                "properties": {
                "$os": sys.platform,
                "$browser": "bot",
                "$device": "bot"
                }
            }
        }
        data = json.dumps(data)

        await self.ws.send(data)

    async def handler(self):
        await self.identify()
        while True:
            msg = await self.ws.recv()
            msg = json.loads(msg)
            await self.consumer(msg)

    async def consumer(self, msg: dict):
        op = msg["op"]

        if op == 0: # Dispatch
            self.opcode0(msg)
        elif op == 7: # Reconnect
            print(msg)
        elif op == 9: # Invalid Session
            print(msg)
        elif op == 10: # Hello
            self.heartbeat_interval = int(msg['d']["heartbeat_interval"])/1000
            asyncio.create_task(self.heartbeat())
        elif op == 11: #Heartbeat ACK
            asyncio.create_task(self.heartbeat())
        else:
            print(msg)

    def opcode0(self, msg: dict):
        t = msg['t']
        if t == "READY":
            print("Bot ready")
        elif t == "MESSAGE_CREATE": # Reading New Message
            print(msg)
        elif t == "GUILD_CREATE":
            pass
        elif t == "INTERACTION_CREATE":
            pass
        else:
            print(msg)

    async def heartbeat(self):
        await asyncio.sleep(self.heartbeat_interval)

        data = {
            "op": 1,
            'd': None
        }
        data = json.dumps(data)

        await self.ws.send(data)

class Route:
    def __init__(self, method: str, path: str):
        self.url = "https://discord.com/api/v9" + path
        self.method = method

class RestAPI:
    def __init__(self, BOT_TOKEN: str):
        self.headers = dict()
        self.headers['authorization'] = "Bot " + BOT_TOKEN

    async def request(self, route: Route, **kwargs: any):
        payload = None
        if "payload" in kwargs:
            payload = kwargs["payload"]

        async with aiohttp.request(route.method, route.url, headers=self.headers, data=payload) as resp:
            print(await resp.text())