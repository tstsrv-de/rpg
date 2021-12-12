import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string


class Consumer(AsyncWebsocketConsumer):
    
    mycounter = 0
    
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.msg_group_name = 'game-%s' % self.game_id

        await self.channel_layer.group_add(
            self.msg_group_name,
            self.channel_name
        )
        
        await self.accept()
                
        await self.channel_layer.group_send(
            self.msg_group_name, 
            {
                'type': 'msg_group_send_init',
            }
        )

    async def msg_group_send_init(self, event):
        await self.channel_layer.group_send(
            self.msg_group_name, { 'type': 'msg_group_send_content',  } 
        )
        
    async def msg_group_send_content(self, event):

        html = render_to_string('game_content.html', {'mycounter': str(self.mycounter)})


        await self.send(text_data=json.dumps({ # send data update
            'game_websocket_content': str(html),
        }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.msg_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['msg']
        game_id = text_data_json['game_id']

        if message == 'alive':
            # (TODO!) update timestamps, delete old entrys
            # check timestamps, delete old and zombie  entrys
            self.mycounter = self.mycounter+1
            print("alive, game-id: " + str(game_id) + " and counter " + str(self.mycounter))
           
            await self.channel_layer.group_send(
                self.msg_group_name, { 
                                        'type': 'msg_group_send_content',  
                                        'game_id' : game_id,
                                        } 
            )            
        


    async def msg_group_do_send(self, event):
        message = event['game_websocket_content']
        game_id = event['game_id']

        await self.send(text_data=json.dumps({
            'game_websocket_content': message,
            'game_id' : game_id,
        }))
        