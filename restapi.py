import aiohttp
import asyncio

class restapi:
    def __init__(self, BOT_TOKEN: str):
        self.token = BOT_TOKEN

    def send_message(self, CHANNEL_ID: int, msg: str):
        payload = {
            "content": msg,
            "tts": False,
        }
        asyncio.run(self.post(CHANNEL_ID, payload))

    async def post(self, CHANNEL_ID: int, payload: dict):
        async with aiohttp.ClientSession() as session:
            header = {"authorization": "Bot " + self.token}
            async with session.post("https://discord.com/api/v9/channels/"+str(CHANNEL_ID)+"/messages", data=payload, headers=header) as res:
                print(await res.text())
