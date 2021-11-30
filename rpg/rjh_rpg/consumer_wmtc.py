import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rjh_rpg.models import HelperCounter
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


class Consumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.msg_group_name = 'wmtc'

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

        wmtc_counter = await sync_to_async(HelperCounter.objects.get_or_create)(name='wmtc')
        wmtc_current_count = str(wmtc_counter[0].count)
        
        if message == 'alive':
            await self.channel_layer.group_send(
                self.msg_group_name,
                {
                    'type': 'msg_group_do_send',
                    'msg': wmtc_current_count,
                }
            )
        if message == 'add_one':
            await self.addone()

    @database_sync_to_async 
    def addone(self):
        wmtc_counter = HelperCounter.objects.get_or_create(name='wmtc')
        wmtc_current_count = str(wmtc_counter[0].count)
        wmtc_counter[0].count = int(wmtc_current_count) + 1
        wmtc_counter[0].save()

    async def msg_group_do_send(self, event):
        message = event['msg']

        await self.send(text_data=json.dumps({
            'msg': message,
        }))

    pass