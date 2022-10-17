import aiohttp
import asyncio


class Route:
    def __init__(self, method: str, path: str) -> None:
        self.url = "https://discord.com/api/v9" + path
        self.method = method


class RestAPI:
    def __init__(self, BOT_TOKEN: str) -> None:
        self.headers = dict()
        self.headers['authorization'] = "Bot " + BOT_TOKEN

    async def request(self, route: Route, **kwargs: any) -> None:
        payload = None
        if "payload" in kwargs:
            payload = kwargs["payload"]

        async with aiohttp.request(route.method, route.url, headers=self.headers, json=payload) as response:
            # print(await response.text())
            pass

    def sendInChannel(self, channel_id: int, payload: str) -> None:
        route = Route("POST", f"/channels/{channel_id}/messages")
        asyncio.create_task(self.request(route, payload=payload))

    def editMessage(self, message_id: int, channel_id: int, payload: str) -> None:
        route = Route("PATCH", f"/channels/{channel_id}/messages/{message_id}")
        asyncio.create_task(self.request(route, payload=payload))
