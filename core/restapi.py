import aiohttp
import asyncio

from core.route import Route


class RestAPI:
    def __init__(self, BOT_TOKEN: str) -> None:
        self.headers = dict()
        self.headers["authorization"] = f"Bot {BOT_TOKEN}"

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
