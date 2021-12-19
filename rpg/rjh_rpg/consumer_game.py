import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string
from rjh_rpg.consumer_game_tools import db_set_game_id_to_finished
from rjh_rpg.consumer_game_tools import db_get_is_game_id_finished

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
                        
        # first send of content on new connection 
        await self.channel_layer.group_send(
            self.msg_group_name, { 'type': 'msg_group_send_content', }
            )
        
    async def msg_group_send_content(self, event):
        # here is where the game logic happens and the rendereing takes place
        
        show_endscreen = await db_get_is_game_id_finished(self.game_id)
        if show_endscreen:
            html = render_to_string('game_endscreen.html')
        else:
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

        if message == 'alive':
            # (TODO!) update timestamps, delete old entrys
            # check timestamps, delete old and zombie  entrys
            
            self.mycounter = self.mycounter+1
            print("alive, game-id: " + str(self.game_id) + " self_game_id: " + str(self.game_id) +  " and counter " + str(self.mycounter))
           
            await self.channel_layer.group_send(self.msg_group_name, { 
                                'type': 'msg_group_send_content',  
                                'game_id' : self.game_id,
                                })

        if message == 'set_game_to_finished':
           
            set_game_to_finished = await db_set_game_id_to_finished(self.game_id)
           
            print("set game to finished, game-id: " + str(self.game_id) + " and its return value was: " + str(set_game_to_finished))

            await self.channel_layer.group_send(self.msg_group_name, { 
                                'type': 'msg_group_send_content',  
                                'game_id' : self.game_id,
                                })


