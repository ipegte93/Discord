import aiohttp
import json

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

        async with aiohttp.request(route.method, route.url, headers=self.headers, json=payload) as response:
            print(await response.text())