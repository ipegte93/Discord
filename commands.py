import asyncio

from core import RestAPI
from core import Route

from mule import mule_search

from utils.components import Components
from utils.message import Message
from utils.get_def_name_list import getDefNameList

class Commands:
    def __init__(self, msg: Message, BOT_TOKEN: str):
        self.__command_prefix = '!'
        self._COMMAND_PREFIX = '!'
        self.__msg = msg
        self._api = RestAPI(BOT_TOKEN)

        content = self.__msg.content
        if len(content) == 0:
            return
            
        if content[0] == self._COMMAND_PREFIX:
            content = content[1:].split(" ")
            if content[0] in getDefNameList(self):
                if len(content) == 1:
                    args = None
                else:
                    args = content[1:]
   
                func = getattr(Commands, content[0])
                try:
                    func(self, args)
                except:
                    func(self)

    def help(self, args):
        if args == None:
            payload = {}
            data = ""
            for method in dir(self):
                if method.startswith('_') is False:
                    data += method + ", "

            data = data[:-2]
            payload["content"] = data

            self._api.sendInChannel(self.__msg.chaneel_id, payload)

    def ping(self):
        payload = {}
        payload["content"] = "pong"

        self._api.sendInChannel(self.__msg.chaneel_id, payload)

    def update(self):
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
            Components.make(type=2, label="Style3", style=3, custom_id="s3"),
            Components.make(type=2, label="Style4", style=4, custom_id="s4"),
        )

        payload["components"] = components.get()

        print(payload)

        self._api.sendInChannel(self.__msg.chaneel_id, payload)

    def mule(self, args):
        payload = {}
        args.append("")
        args.append("")
        if args == None or args[2] == "" or args[1] == "":
            payload["content"] = "오류: 씨발년아 제대로 적으삼"
        else:
            content = mule_search(args[0], args[1], args[2])
            payload["content"] = content

        self._api.sendInChannel(self.__msg.chaneel_id, payload)

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


