import asyncio
from restapi import *

class Message:
    def __init__(self, author, content, message_id, channel_id):
        self.author = author
        self.content = content
        self.message_id = message_id
        self.chaneel_id = channel_id

class Commands:
    def __init__(self, msg: Message, BOT_TOKEN: str):
        self.TOKEN = BOT_TOKEN
        self.__command_prefix = '!'
        self.msg = msg

        for method in dir(self):
            if method.startswith('--') is False:
                if self.msg.content == self.__command_prefix + method:
                    func = getattr(Commands, method)
                    func(self)

    def ping(self):
        payload = {}
        payload["content"] = "pong"
        http = RestAPI(self.TOKEN)
        asyncio.create_task(http.request(Route("POST", "/channels/{}/messages".format(self.msg.chaneel_id)),payload=payload))

class ResponseHandler:
    def __init__(self, response: dict, BOT_TOKEN: str):
        self.TOKEN = BOT_TOKEN
        self.__handler(response)

    def __handler(self, response: dict):
        if response['t'] == "MESSAGE_CREATE":
            self.__parser(response)
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
