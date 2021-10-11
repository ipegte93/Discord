# TOKEN = "<YOUR BOT TOKEN>"
TOKEN = ""

if TOKEN == "":
    import sys
    TOKEN = sys.argv[1]
    if TOKEN == "":
        print("TOKEN not valid!")
        exit()

import asyncio
from core import DiscordWebsocket

async def main():
    ws = DiscordWebsocket(TOKEN)
    await ws.connect()

asyncio.run(main())