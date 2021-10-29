import asyncio
from core import RestAPI
from core import Route

from mule import mule_search
from component import *

class Message:
    def __init__(self, author, content, message_id, channel_id):
        self.author = author
        self.content = content
        self.message_id = message_id
        self.chaneel_id = channel_id

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
        for text in args:
            msg += text + " "
        msg += "그게 뭔데 씹덕새끼야"

        payload = {}
        payload["content"] = msg

        http = RestAPI(self.__TOKEN)
        asyncio.create_task(http.request(Route("POST", "/channels/{}/messages".format(self.__msg.chaneel_id)),payload=payload))

    def test2(self):
        payload = {}
        
        http = ResrAPI(self.__token)
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

class ResponseHandler:
    def __init__(self, response: dict, BOT_TOKEN: str):
        self.TOKEN = BOT_TOKEN
        self.__handler(response)

    def __handler(self, response: dict):
        res = response['t']
        if res == "MESSAGE_CREATE":
            self.__parser(response)
        elif res == "GUILD_CREATE":
            pass
        else:
            print(response)

    def __parser(self, response: dict):
        author = response['d']["author"]
        del author["public_flags"]
        del author["discriminator"]
        del author["avatar"]

        content = response['d']["content"]
        message_id = response['d']["id"]
        channel_id = response['d']["channel_id"]

        msg = Message(author, content, message_id, channel_id)
        Commands(msg, self.TOKEN)
