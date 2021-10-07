import asyncio

class Message:
    def __init__(self, author, content, message_id):
        self.author = author
        self.content = content
        self.message_id = message_id

class Commands:
    def __init__(self, msg: Message):
        self.__command_prefix = '!'

        for method in dir(self):
            if method.startswith('--') is False:
                if msg.content == self.__command_prefix + method:
                    func = getattr(Commands, method)
                    func(self)

    def ping(self):
        print("ping 명령어 감지")

class ResponseHandler:
    def __init__(self, response: dict):
        self.__handler(response)

    def __handler(self, response: dict):
        if response['t'] == "MESSAGE_CREATE":
            self.__parser(response)

    def __parser(self, response: dict):
        author = response['d']["author"]
        del author["public_flags"]
        del author["discriminator"]
        del author["avatar"]

        content = response['d']["content"]
        message_id = response['d']["id"]

        msg = Message(author, content, message_id)
        Commands(msg)
