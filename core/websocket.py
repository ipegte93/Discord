import asyncio
import websockets
import json
import sys

from .response_handler import ResponseHandler

class DiscordWebsocket:
    def __init__(self, BOT_TOKEN: str):
        self.TOKEN = BOT_TOKEN
        self.responseHandler = ResponseHandler(BOT_TOKEN)

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
            self.responseHandler.handle(response)
        elif op == 7: # Reconnect
            print(response)
        elif op == 9: # Invalid Session
            print("bot can't connect!")
            exit()
        elif op == 10: # Hello
            self.heartbeat_interval = int(response['d']["heartbeat_interval"])/1000
            asyncio.create_task(self.__heartbeat())
        elif op == 11: #Heartbeat ACK
            asyncio.create_task(self.__heartbeat())
        else:
            print(response)

    async def __heartbeat(self):
        await asyncio.sleep(self.heartbeat_interval)

        payload = {
            "op": 1,
            'd': None
        }
        payload = json.dumps(payload)

        await self.ws.send(payload)
