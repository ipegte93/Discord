import asyncio
from core import RestAPI
from core import Route
from core.message import Message

from mule import mule_search
from component import *

class Commands:
    def __init__(self, msg: Message, BOT_TOKEN: str):
        self.__TOKEN = BOT_TOKEN
        self.__command_prefix = '!'
        self.__msg = msg

        content = self.__msg.content
        if len(content) == 0:
            return

        if content[0] == self.__command_prefix:
            content = content[1:].split(" ")
            for method in dir(self):
                if method.startswith("_") is False:
                    if content[0] == method:
                        if len(content) == 1:
                            args = None
                        else:
                            args = content[1:]
                        func = getattr(Commands, method)
                        func(self, args)

    def help(self, args):
        if args == None:
            payload = {}
            data = ""
            for method in dir(self):
                if method.startswith('_') is False:
                    data += method + ", "

            data = data[:-2]
            payload["content"] = data

            http = RestAPI(self.__TOKEN)
            asyncio.create_task(http.request(Route("POST", "/channels/{}/messages".format(self.__msg.chaneel_id)),payload=payload))

    def ping(self, args):
        payload = {}
        payload["content"] = "pong"

        http = RestAPI(self.__TOKEN)
        asyncio.create_task(http.request(Route("POST", "/channels/{}/messages".format(self.__msg.chaneel_id)),payload=payload))

    def update(self, args):
        exit()

    def test(self, args):
        msg = "시발년아 "
        if args is not None:
            for text in args:
                msg += text + " "
        msg += "그게 뭔데 씹덕새끼야"

        payload = {}
        payload["content"] = msg

        components = Components()
        components.addActionRow(
            Components.make(type=2, label="Click!", style=1, custom_id="click"),
            Components.make(type=2, label="Sex!", style=1, custom_id="sex!"),
        )

        payload["components"] = components.get()

        print(payload)

        http = RestAPI(self.__TOKEN)
        asyncio.create_task(http.request(Route("POST", "/channels/{}/messages".format(self.__msg.chaneel_id)),payload=payload))

    def mule(self, args):
        payload = {}
        args.append("")
        args.append("")
        if args == None or args[2] == "" or args[1] == "":
            payload["content"] = "오류: 씨발년아 제대로 적으삼"
        else:
            content = mule_search(args[0], args[1], args[2])
            payload["content"] = content

        http = RestAPI(self.__TOKEN)
        asyncio.create_task(http.request(Route("POST", "/channels/{}/messages".format(self.__msg.chaneel_id)),payload=payload))
