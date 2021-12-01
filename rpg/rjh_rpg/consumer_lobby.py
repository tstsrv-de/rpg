import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rjh_rpg.models import HelperCounter
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from rjh_rpg.models import GameScenes, LobbySlots


class Consumer(AsyncWebsocketConsumer):
    
    html_table_top = """
    <h1>**scene_name**</h1>
    <table class="table table-bordered table-striped">
    <tr>
    
    """
    
    html_placeselector_used = """
    
    <td>
    <input class="form-control" style="min-width: 0;width: auto;" type="text" id="slot_id_**slot_id" name="slot_id_**slot_id" value="**slot_id_char_name**" disabled><br />
    <input class="btn btn-primary" type="submit" value="Platz freigeben">
    </td>
    
    """    
    html_placeselector_free = """
    <td>
    <input class="form-control" style="min-width: 0;width: auto;" type="text" id="slot_id_**slot_id**" name="slot_id_**slot_id" value="" disabled><br />
    <input class="btn btn-primary" type="submit" value="Platz nehmen">
    </td>
    """    
    
    html_table_bottom = """
    </tr>
    </table>
    
    """
    
    
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
                'type': 'msg_group_send_init',
            }
        )

    async def msg_group_send_init(self, event):
        await self.send(text_data=json.dumps({ # send data init
            'lobby_msg': 'Counter init...',
        }))
        
    async def msg_group_send_content(self, event):
        
        scene_name = await self.db_get_scene_name()
        html = self.html_table_top.replace("**scene_name**",scene_name) 
        num_players = await self.db_get_num_players()
        
        for slot_id in range(num_players):
            if slot_id != 0 and slot_id % 3 == 0: # linebreak in table every 4 slots
                html = html + "</tr><tr>"
            
            slot_state = await self.db_get_slot_state(slot_id)
            
            if  slot_state == 1:
                slot_template = self.html_placeselector_used
                slot_insert = slot_template.replace('**slot_id**',str(slot_id))
                slot_insert = slot_template.replace('**slot_id_char_name**','willi wanka')
                
                
            else:
                slot_template = self.html_placeselector_free
                slot_insert = slot_template.replace('**slot_id**',str(slot_id))
            html = html + slot_insert 
        html = html + self.html_table_bottom
        
        
        await self.send(text_data=json.dumps({ # send data update
            'lobby_msg': str(html),
        }))
                

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.msg_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['lobby_msg']

        lobby_counter = await sync_to_async(HelperCounter.objects.get_or_create)(name=self.msg_group_name)
        lobby_current_count = str(lobby_counter[0].count)
        
        if message == 'heartbeat':
            await self.channel_layer.group_send(
            self.msg_group_name, 
            {
                'type': 'msg_group_send_content',
            }
        )

            #num_players = await self.get_number_of_players_in_scene()
            #await self.channel_layer.group_send(
            #    self.msg_group_name,
            #    {
            #        'type': 'msg_group_do_send',
            #        'lobby_msg': '<h1>'+lobby_current_count+'</h1> <h2>' + str(num_players) + '</h2>',
            #    }
            #)
        if message == 'take_slot':
            slot_id_to_take = text_data_json['lobby_msg']
            await self.addone()

    @database_sync_to_async 
    def addone(self):
        lobby_counter = HelperCounter.objects.get_or_create(name=self.msg_group_name)
        lobby_current_count = str(lobby_counter[0].count)
        lobby_counter[0].count = int(lobby_current_count) + 1
        lobby_counter[0].save()

    async def msg_group_do_send(self, event):
        message = event['lobby_msg']

        await self.send(text_data=json.dumps({
            'lobby_msg': message,
        }))
        
    @database_sync_to_async     
    def db_get_num_players(self):
        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        scene = GameScenes.objects.filter(id=self.scene_id) # place 0 = worldmap
        num_players = scene[0].req_players
        return num_players

    @database_sync_to_async     
    def db_get_scene_name(self):
        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        scene = GameScenes.objects.filter(id=self.scene_id) # place 0 = worldmap
        scene_name = scene[0].name
        return scene_name

    @database_sync_to_async     
    def db_get_slot_state(self, slot_id):
        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        if LobbySlots.objects.filter(game_scene_id=self.scene_id, slot_id=slot_id).exists():
            return 1
        else:
            return 0
    


    pass