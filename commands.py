import asyncio
from core import RestAPI
from core import Route

from mule import mule_search

class Message:
    def __init__(self, author, content, message_id, channel_id):
        self.author = author
        self.content = content
        self.message_id = message_id
        self.chaneel_id = channel_id

class Components:
    def __init__(self):
        self.components = []

    @staticmethod
    def make(**kwargs):
        return kwargs

    def addActionRow(self, *args):
        data = []
        for temp in args:
            data.append(temp)

        self.components.append(
            self.make(type=1, components=data)
        )

    def get(self):
        return self.components

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
        components.addActionRow(
            Components.make(type=2, label="Style1", style=1, custom_id="s1"),
            Components.make(type=2, label="Style2", style=2, custom_id="s2"),
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

#https://discord.com/developers/docs/interactions/receiving-and-responding#responding-to-an-interaction
class ComponentCallback:
    def __init__(self, BOT_TOKEN, data, id, token):
        self.BOT_TOKEN = BOT_TOKEN
        self.interaction_id = id
        self.interaction_token = token

    def type4(self): #DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
        payload = {}
        payload["type"] = 4
        payload["data"] = {
            "content": "굳"
        }

        http = RestAPI(self.BOT_TOKEN)
        asyncio.create_task(http.request(Route("POST", "/interactions/{}/{}/callback".format(self.interaction_id, self.interaction_token)),payload=payload))

    def type6(self): #DEFERRED_UPDATE_MESSAGE
        pass

    def type7(self): #UPDATE_MESSAGE
        pass

    def type8(self): #APPLICATION_COMMAND_AUTOCOMPLETE_RESULT
        pass


