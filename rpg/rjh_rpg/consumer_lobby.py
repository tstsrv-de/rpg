import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rjh_rpg.models import HelperCounter
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


class Consumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['scene_id']
        #self.room_group_name = 'lobby-%s' % self.room_name
        self.msg_group_name = 'lobby-%s' % self.room_name

        await self.channel_layer.group_add(
            self.msg_group_name,
            self.channel_name
        )
        
        await self.accept()
                
        await self.channel_layer.group_send(
            self.msg_group_name, 
            {
                'type': 'msg_group_do_init',
            }
        )

    async def msg_group_do_init(self, event):
        await self.send(text_data=json.dumps({
            'msg': 'Counter init...',
        }))
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.msg_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['msg']

        lobby_counter = await sync_to_async(HelperCounter.objects.get_or_create)(name=self.msg_group_name)
        lobby_current_count = str(lobby_counter[0].count)
        
        if message == 'alive':
            await self.channel_layer.group_send(
                self.msg_group_name,
                {
                    'type': 'msg_group_do_send',
                    'msg': lobby_current_count,
                }
            )
        if message == 'add_one':
            await self.addone()

    @database_sync_to_async 
    def addone(self):
        lobby_counter = HelperCounter.objects.get_or_create(name=self.msg_group_name)
        lobby_current_count = str(lobby_counter[0].count)
        lobby_counter[0].count = int(lobby_current_count) + 1
        lobby_counter[0].save()

    async def msg_group_do_send(self, event):
        message = event['msg']

        await self.send(text_data=json.dumps({
            'msg': message,
        }))

    pass