import asyncio
import websockets
import json
import sys
import aiohttp

from commands import ResponseHandler

class Websocket:
    def __init__(self, BOT_TOKEN: str):
        self.TOKEN = BOT_TOKEN

    def start(self):
        asyncio.run(self.connect())

    async def connect(self):
        async with websockets.connect("wss://gateway.discord.gg") as self.ws:
            await self.__handler()

    async def __handler(self):
        await self.__identify()
        while True:
            response = await self.ws.recv()
            response = json.loads(response)
            await self.__consumer(response)

    async def __identify(self):
        payload = {
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
        payload = json.dumps(payload)

        await self.ws.send(payload)

    async def __consumer(self, response: dict):
        op = response["op"]

        if op == 0: # Dispatch
            self.__dispatch(response)
        elif op == 7: # Reconnect
            print(response)
        elif op == 9: # Invalid Session
            print(response)
        elif op == 10: # Hello
            self.heartbeat_interval = int(response['d']["heartbeat_interval"])/1000
            asyncio.create_task(self.__heartbeat())
        elif op == 11: #Heartbeat ACK
            asyncio.create_task(self.__heartbeat())
        else:
            print(response)

    def __dispatch(self, response: dict):
        if response['t'] == "READY":
            print("Bot ready")
        else:
            ResponseHandler(response)

    async def __heartbeat(self):
        await asyncio.sleep(self.heartbeat_interval)

        payload = {
            "op": 1,
            'd': None
        }
        payload = json.dumps(payload)

        await self.ws.send(payload)

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

        async with aiohttp.request(route.method, route.url, headers=self.headers, data=payload) as response:
            print(await response.text())