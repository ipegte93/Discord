from core.restapi import *

from mule import mule_search

from utils.components import Components
from utils.message import Message
from utils.get_def_name_list import getDefNameList
from utils.interaction import InteractionDict

class Commands:
    def __init__(self, msg: Message, BOT_TOKEN: str):
        self._COMMAND_PREFIX = '!'
        self._msg = msg
        self._api = RestAPI(BOT_TOKEN)

        content = self._msg.content
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

    def help(self):
        payload = {}
        content = ""

        for element in getDefNameList(self):
            content += element + ", "
        content = content[:-2]
        payload["content"] = content

        self._api.sendInChannel(self._msg.channel_id, payload)

    def ping(self):
        payload = {}
        payload["content"] = "pong"

        self._api.sendInChannel(self._msg.channel_id, payload)

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

        self._api.sendInChannel(self._msg.channel_id, payload)

    def mule(self, args):
        payload = {}
        args.append("")
        args.append("")
        if args == None or args[2] == "" or args[1] == "":
            payload["content"] = "오류: 씨발년아 제대로 적으삼"
        else:
            content = mule_search(args[0], args[1], args[2])
            payload["content"] = content

        self._api.sendInChannel(self._msg.channel_id, payload)

class InteractionResponse:
    def __init__(self, interactionDict: InteractionDict):
        self.payload = {}
        self.interactionDict = interactionDict

    def _getPayload(self):
        return self.payload