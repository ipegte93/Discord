# TOKEN = "<YOUR BOT TOKEN>"
TOKEN = None

if TOKEN == None:
    import sys
    try:
        TOKEN = sys.argv[1]

    except:
        print("Token invalid")
        exit()

import asyncio
from core import DiscordWebsocket

async def main():
    ws = DiscordWebsocket(TOKEN)
    await ws.connect()

asyncio.run(main())