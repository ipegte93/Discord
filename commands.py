from core.restapi import *

from mule import *

from utils.components import Components
from utils.struct import *
from utils.get_def_name_list import getDefNameList

class Commands:
    def __init__(self, BOT_TOKEN: str):
        self._COMMAND_PREFIX = '!'
        self._api = RestAPI(BOT_TOKEN)
        self._inputMode = 0

        if self._inputMode > 0:
            self._inputMode -= 1
            self._input()

    def _check(self, messageStruct: MessageStruct):
        content = messageStruct.content
        if len(content) == 0:
            return

        elif content[0] == self._COMMAND_PREFIX:
            self._messageStruct = messageStruct

            content = content[1:].split(" ")
            if content[0] in getDefNameList(self):
                func = getattr(Commands, content[0])
                if len(content) == 1:
                    args = None
                else:
                    args = content[1:]
                try:
                    func(self)
                except:
                    func(self, args)

    def _input(self):
        print(self._messageStruct.content)

    def help(self):
        payload = {}
        content = ""

        for element in getDefNameList(self):
            content += element + ", "
        content = content[:-2]
        payload["content"] = content

        self._api.sendInChannel(self._messageStruct.channel_id, payload)

    def ping(self):
        payload = {}
        payload["content"] = "pong"

        self._api.sendInChannel(self._messageStruct.channel_id, payload)

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

        self._api.sendInChannel(self._messageStruct.channel_id, payload)

    def mule(self, args):
        payload = {}
        args.append("")
        args.append("")
        if args == None or args[2] == "" or args[1] == "":
            payload["content"] = "오류: 씨발년아 제대로 적으삼"
        else:
            content = mule_search(args[0], args[1], args[2])
            payload["content"] = content

        self._api.sendInChannel(self._messageStruct.channel_id, payload)

    def new_mule(self, args):
        if args is None:
            self.mule = Mule()
        else:
            self.mule = Mule(search=args[0])

        payload = self.mule.template()
        self._api.sendInChannel(self._messageStruct.channel_id, payload)

class InteractionResponse:
    def __init__(self, interactionStruct: InteractionStruct):
        self.payload = {}
        self.interactionStruct = interactionStruct

        if interactionStruct.custom_id in getDefNameList(self):
            func = getattr(InteractionResponse, interactionStruct.custom_id)
            func(self)
        else:
            self.payload["type"] = 4
            self.payload["data"] = {
                "content": "오류: 씨발 이거 기능 없음 -> custom_id: " + interactionStruct.custom_id
            }

    def _getPayload(self):
        return self.payload

    def mule_min_price(self):
        self.payload["type"] = 6

    def mule_max_price(self):
        self.payload["type"] = 6

    def mule_search(self):
        self.payload["type"] = 6