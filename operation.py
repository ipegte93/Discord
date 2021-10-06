import aiohttp
import asyncio

class route:
    def __init__(self, method: str, path: str, **kwargs):
        self.url = "https://discord.com/api/v9/channels/" + path
        self.method = method

class restapi:
    def __init__(self, BOT_TOKEN: str):
        self.headers = dict()
        self.headers['authorization'] = "Bot" + BOT_TOKEN

    async def request(self, route: route, **kwargs):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            payload = None
            if "payload" in kwargs:
                payload = kwargs["payload"]

            async with session.request(route.method, route.url, data=payload) as resp:
                print(await resp.text())



    async def post(self, url: str, payload: dict):
        resp = await self.session.post(url, data=payload)
        async with resp:
            print(await resp.text())