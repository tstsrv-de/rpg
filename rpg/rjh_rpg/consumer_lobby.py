import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rjh_rpg.models import HelperCounter
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from rjh_rpg.models import GameScenes, LobbySlots
from django.contrib.auth.models import User
from rjh_rpg.models import GameState
from rjh_rpg.models import UserChar

class Consumer(AsyncWebsocketConsumer):
    
    html_table_top = """
    <h1>**scene_name**</h1>
    <table class="table table-bordered table-striped">
    <tr>
    
    """
    
    html_placeselector = """
    
    <td>
    <input class="form-control" style="min-width: 0;width: auto;" type="text" id="slot_id_**slot_id**" name="slot_id_**slot_id**" value="**slot_id_char_name**" disabled><br />
    <input class="btn btn-primary" type="submit" value="**button_text**" onclick="**js_button_function**(**slot_id**);" **button_disabled**>
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
        await self.channel_layer.group_send(
            self.msg_group_name, { 'type': 'msg_group_send_content',  } 
        )
        
    async def msg_group_send_content(self, event):
        
        
        scene_name = await self.db_get_scene_name()
        html = self.html_table_top.replace("**scene_name**",scene_name) 
        num_players = await self.db_get_num_players()
        
        for slot_id in range(num_players):
            if slot_id != 0 and slot_id % 3 == 0: # linebreak in table every 4 slots
                html = html + "</tr><tr>"
            
            slot_state = await self.db_get_slot_state(slot_id)
    
            slot_template = self.html_placeselector
            slot_template = slot_template.replace('**slot_id**',str(slot_id))            
            
            char_name = ""
            slot_char_id = await self.db_get_slot_char_id(slot_id)
            
            if  slot_state == 1:
                char_name = await self.db_get_slot_char_name(slot_id)
                slot_template = slot_template.replace('**js_button_function**','free_the_slot')
                slot_template = slot_template.replace('**button_text**','Platz freigeben')
                # check if own entry or not, disable button if it is so
                #if slot_char_id == self.char_id:
                slot_template = slot_template.replace('**button_disabled**','')
                #else:
                #    slot_template = slot_template.replace('**button_disabled**','disabled')
                    
                
                #slot_template = slot_template.replace('**button_disabled**','')
            else:
                slot_template = slot_template.replace('**js_button_function**','take_the_slot')
                slot_template = slot_template.replace('**button_text**','Platz belegen')
                slot_template = slot_template.replace('**button_disabled**','')
                
            slot_template = slot_template.replace('**slot_id_char_name**',char_name)
                
            html = html + slot_template 
        html = html + self.html_table_bottom
        html = html.replace('\n','')
        
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

        if message == 'heartbeat':
            # (TODO!) update timestamps, delete old entrys
            pass

        if message == 'free_the_slot':

            #text_data_json = json.loads(text_data)
            char_id = text_data_json['char_id']
            slot_id = text_data_json['slot_id']
            
            set_new_char_to_slot = await self.db_free_slot(slot_id, char_id)
            print(set_new_char_to_slot)
            
            await self.channel_layer.group_send(
                self.msg_group_name, { 'type': 'msg_group_send_content', 'char_id' : char_id,  } 
            )            
        
        if message == 'take_the_slot':
            #text_data_json = json.loads(text_data)
            char_id = text_data_json['char_id']
            slot_id = text_data_json['slot_id']
            
            set_new_char_to_slot = await self.db_set_char_to_slot(slot_id, char_id)
            print(set_new_char_to_slot)
                     
            await self.channel_layer.group_send(
                self.msg_group_name, { 'type': 'msg_group_send_content',  'char_id' : char_id, } 
            )            


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
            return 1 #used
        else:
            return 0 #free
    
    @database_sync_to_async     
    def db_get_slot_char_name(self, slot_id):
        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        if LobbySlots.objects.filter(game_scene_id=self.scene_id, slot_id=slot_id).exists():
            char_name = LobbySlots.objects.filter(game_scene_id=self.scene_id, slot_id=slot_id)
            return str(char_name[0].user_char_id.name)
        else:
            return "Error"

    @database_sync_to_async     
    def db_get_slot_char_id(self, slot_id):
        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        if LobbySlots.objects.filter(game_scene_id=self.scene_id, slot_id=slot_id).exists():
            char_id = LobbySlots.objects.filter(game_scene_id=self.scene_id, slot_id=slot_id)
            return int(char_id[0].user_char_id.id)
        else:
            return "Error"

    @database_sync_to_async     
    def db_set_char_to_slot(self, slot_id, char_id):
        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        
        new_lobby_slot = LobbySlots()
        
        new_lobby_slot.slot_id = slot_id

        char_id_obj = UserChar.objects.filter(id=char_id)
        new_lobby_slot.user_char_id = char_id_obj[0]
        
        scene_id_obj = GameScenes.objects.filter(id=self.scene_id) # place 0 = worldmap        
        new_lobby_slot.game_scene_id = scene_id_obj[0]
        
        try: 
            new_lobby_slot.save()
            if LobbySlots.objects.filter(game_scene_id=self.scene_id, slot_id=slot_id).exists():
                char_name = LobbySlots.objects.filter(game_scene_id=self.scene_id, slot_id=slot_id)
                return "save: ok"
            else:
                return "save: error"
        except:
            return "save: double"

    @database_sync_to_async     
    def db_free_slot(self, slot_id, char_id):

        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        try:
            LobbySlots.objects.get(game_scene_id=self.scene_id, slot_id=slot_id, user_char_id=char_id).delete()
        except:
            return "delete: alien char_id"

        try: 
            if LobbySlots.objects.filter(game_scene_id=self.scene_id, slot_id=slot_id).exists():
                char_name = LobbySlots.objects.filter(game_scene_id=self.scene_id, slot_id=slot_id)
                return "delete: still there"
            else:
                return "delete: ok"
        except:
            return "delele: wierd error"

    pass