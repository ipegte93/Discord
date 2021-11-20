class MessageStruct:
    def __init__(self, author, content, message_id, channel_id):
        self.author = author
        self.content = content
        self.message_id = message_id
        self.channel_id = channel_id

class InteractionStruct:
    def __init__(self, custom_id, component_type, interaction_id, interaction_token):
        self.custom_id = custom_id
        self.component_type = component_type
        self.interaction_id = interaction_id
        self.interaction_token = interaction_token