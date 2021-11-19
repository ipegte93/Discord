from commands import Commands, ComponentCallback
from utils.message import Message

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
        elif res == "INTERACTION_CREATE":
            if response['d']["type"] == 3:
                data = response['d']["data"]
                interaction_id = response['d']["id"]
                interaction_token = response['d']["token"]

                callback = ComponentCallback(self.TOKEN, data, interaction_id, interaction_token)
                callback.type4()
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