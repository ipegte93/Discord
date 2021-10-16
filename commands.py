import asyncio
from core import RestAPI
from core import Route

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

        for method in dir(self): #message를 스페이스로 slice() 해서 args로 넘기는 기능 만들고 있음
            if method.startswith('_') is False:
                if self.__msg.content == self.__command_prefix + method:
                    func = getattr(Commands, method)
                    func(self)

        if self.__msg.content[0] == self.__command_prefix:
            print("it is commands!")

    def help(self):
        payload = {}
        data = ""
        for method in dir(self):
            if method.startswith('_') is False:
                data += method + ", "

        data = data[:-2]
        payload["content"] = data

        http = RestAPI(self.__TOKEN)
        asyncio.create_task(http.request(Route("POST", "/channels/{}/messages".format(self.__msg.chaneel_id)),payload=payload))

    def ping(self):
        payload = {}
        payload["content"] = "pong"

        http = RestAPI(self.__TOKEN)
        asyncio.create_task(http.request(Route("POST", "/channels/{}/messages".format(self.__msg.chaneel_id)),payload=payload))

    def update(self):
        exit()

    def mule(self):
        pass

    def test(self):
        pass

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
