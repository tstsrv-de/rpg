# from https://github.com/veryacademy/YT-Django-Project-\
# Chatroom-Getting-Started/blob/master/chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rjh_rpg.models import GameState
from channels.db import database_sync_to_async

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'welcome_message',
            }
        )

    async def welcome_message(self, event):
        chars_in_chat = await self.db_get_list_chars_in_chat()

        await self.send(text_data=json.dumps({
            'username': 'Aktuell im Chat',
            'message': chars_in_chat,
        }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @database_sync_to_async     
    def db_get_list_chars_in_chat(self):
        list_of_chars_in_chat = GameState.objects.filter(place=self.room_name).order_by('char')
        char_names = []
        
        for row in list_of_chars_in_chat:
            char_names.append(str(row.char))
            
        return char_names

    pass
