import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import (
    AppUser, Chat, ChatMember, MessageChat
)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.postRequest = {}
        postRequestRaw = self.scope['query_string'].decode().split('&')
        for line in postRequestRaw:
            key, atrib = line.split('=')
            self.postRequest[key] = atrib

        self.chatIdentificator = self.scope['url_route']['kwargs'].get('chat_id')
        self.userIdentificator = self.postRequest.get('user_id')

        if self.chatIdentificator:
            self.roomGroupName = f"chat.{self.chatIdentificator}"
            await self.channel_layer.group_add(
                self.roomGroupName ,
                self.channel_name
            )
            await self.accept()
        else:
            await self.disconnect()
    async def disconnect(self , close_code):
        await self.channel.name.group_discard(
            self.roomGroupName , 
            self.channel_name 
        )
    async def receive(self, text_data):
        data_structure = json.loads(text_data)

        data_structure['server_db_result'] = await manageDataDB_on_server(data_structure)
        await self.channel_layer.group_send(
            self.roomGroupName,
            data_structure
        )
    async def send_message(self , event) :
        data_structure = event

        data_external = {'user_id': self.userIdentificator}
        await manageDataDB_on_server(data_structure, 'read_message_resive', data_external)
        await self.send(text_data = json.dumps({
            'user_id': data_structure['user_id'],
            'username': data_structure['user_name'],
            'message': data_structure['text'],
            'sended_at': data_structure['server_db_result'].sended_at.strftime('%H:%M')
        }))

def send_message_create_db(data, data_external=None):
    msg_chatmember = ChatMember.objects.get(
        chat_id = data['chat_id'],
        user_id = data['user_id'],
    )
    if not (msg_chatmember is None):
        return_data = MessageChat.objects.create(
            chat_id = msg_chatmember.chat_id,
            user_id = msg_chatmember.user_id,
            text = data['text'],
            #datetime = data_structure['datetime'],
        )
        return return_data

def read_message_update_db(data, data_external=None):
    if data_external is None:
        return False
    
    if data['server_db_result'].__class__ == MessageChat:
        message = data['server_db_result']
        reader_user_id = data_external['user_id']
        if reader_user_id != data['user_id']: 
            reader_user = AppUser.objects.get(id=reader_user_id)
            message.readed_by.add(reader_user)
            return True
    return False


database_server_interactions = {
    'send_message': send_message_create_db,
    'read_message_resive': read_message_update_db,
}

@sync_to_async
def manageDataDB_on_server(data, type_interaction=None, data_external=None):
    if len(data) > 0:
        keysfunc = database_server_interactions.keys()

        key = None
        if (type_interaction in keysfunc):
            key = type_interaction
        elif (data['type'] in keysfunc):
            key = data['type']

        if key is not None:
            db_func = database_server_interactions.get(key)
            return db_func(data, data_external)