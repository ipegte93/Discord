import asyncio

from commands import *
from utils.struct import *
from core.restapi import *

class ResponseHandler:
    def __init__(self, BOT_TOKEN: str):
        self.BOT_TOKEN = BOT_TOKEN
        self.commands = Commands(self.BOT_TOKEN)

    def handle(self, response: dict):
        res = response['t']
        if res == "READY":
            print("BOT READY")
        elif res == "MESSAGE_CREATE":
            self.__parser(response)
        elif res == "GUILD_CREATE":
            pass
        elif res == "INTERACTION_CREATE":
            if response['d']["type"] == 3:
                data = response['d']["data"]
                interaction_id = response['d']["id"]
                interaction_token = response['d']["token"]
                interactionStruct = InteractionStruct(data["custom_id"], data["component_type"], interaction_id, interaction_token)

                intracationCallback = InteractionCallback(self.BOT_TOKEN, interactionStruct)
                intracationCallback.callback()

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

        print("<{}> {}".format(author["username"], content))
        if len(response['d']["attachments"]) != 0:
            print("=====Attachment=====")
            for attachment in response['d']["attachments"]:
                print(attachment["url"])

        messageStruct = MessageStruct(author, content, message_id, channel_id)
        self.commands._check(messageStruct)

#https://discord.com/developers/docs/interactions/receiving-and-responding#responding-to-an-interaction
class InteractionCallback:
    def __init__(self, BOT_TOKEN, interactionStruct: InteractionStruct):
        self.BOT_TOKEN = BOT_TOKEN
        self.interactionStruct = interactionStruct

    def callback(self):
        command_response = InteractionResponse(self.interactionStruct)
        payload = command_response._getPayload()

        http = RestAPI(self.BOT_TOKEN)
        asyncio.create_task(http.request(Route("POST", "/interactions/{}/{}/callback".format(self.interactionStruct.interaction_id, self.interactionStruct.interaction_token)),payload=payload))
