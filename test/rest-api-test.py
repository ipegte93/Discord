import aiohttp
import asyncio

data = {
    "content": "Hi",
    "tts": False,
}

head = {
    "authorization": "Bot <Token>"
}

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post("https://discord.com/api/v9/channels/862348023764746279/messages", data=data, headers=head) as res:
            a = await res.text()
            print(a)

asyncio.run(main())