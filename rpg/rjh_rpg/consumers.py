# from https://github.com/veryacademy/YT-Django-Project-\
# Chatroom-Getting-Started/blob/master/chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rjh_rpg.models import GameState
from channels.db import database_sync_to_async
from rjh_rpg.rpg_tools  import rpg_websocket_user_char_chat_heartbeat
from datetime import datetime
from rjh_rpg.rpg_tools import rpg_get_config

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        try:
            message = text_data_json['message']
        except:
            message = ""

        try:
            ul = text_data_json['ul']
        except:
            ul = ""
        
        if ul == 'heatbeat':
            chars_in_chat = await self.db_get_list_chars_in_chat()      
            
            try:
                heartbeat_char_id = text_data_json['char_id']
                await rpg_websocket_user_char_chat_heartbeat(heartbeat_char_id)
            except:
                pass
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ul_message',
                    'ul': chars_in_chat,
                }
            )

        if message != "":
            username = text_data_json['username']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chatroom_message',
                    'message': message,
                    'username': username,
                }
            )
        
    async def ul_message(self, event):
        ul = event['ul']

        await self.send(text_data=json.dumps({
            'ul': ul,
        }))            

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @database_sync_to_async     
    def db_get_list_chars_in_chat(self):
        # (TODO!) Delete users with to old datetime 'lastaction'
        list_of_chars_in_chat = GameState.objects.filter(place=self.room_name).order_by('char')
        current_datetime = int(datetime.now().strftime('%s'))
        chat_timeout = rpg_get_config('chat_timeout')
        char_names = ""
        
        for row in list_of_chars_in_chat:
            last_datetime = int(row.last_chat_heartbeat.strftime('%s'))

            if ((current_datetime - last_datetime)>chat_timeout):
                GameState.objects.filter(char=row.char).delete()
            
            char_names = char_names + str(row.char) + "<br />"
            
        return char_names

    pass
