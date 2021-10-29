# TOKEN = "<YOUR BOT TOKEN>"
TOKEN = "ODk4ODI3NDU1MTg2NDc3MDU3.YWp4TA._IJyaStYPT8yy9U0rcFyw5RIVzs"

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