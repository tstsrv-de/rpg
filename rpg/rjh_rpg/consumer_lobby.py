from datetime import time
import json
from json.encoder import JSONEncoder
from channels.generic.websocket import AsyncWebsocketConsumer
from rjh_rpg.models import HelperCounter
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from rjh_rpg.models import GameScenes, LobbySlots
from django.contrib.auth.models import User
from rjh_rpg.models import GameState
from rjh_rpg.models import UserChar
from django.db.models.functions import Now
from datetime import datetime

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
    
    html_jump_to_game = """
    
    <form action="{% url 'scene_jumper' %}" method="POST" id="interest-select" class="form-inline">
    <div class="form-group">
    {% csrf_token %}

    <select  class="custom-select form-control" size="5" id="scene_id" name="scene_id" >
    {% for scene in game_scenes_list %} 
        <option value={{scene.id}}>{{scene.name}} (Spieler im Chat: {{ scene.players_in_chat_counter }}, davon spielbereit: {{ scene.waiting_players }}/{{ scene.req_players }})</option>
    {% endfor %}
    </select> 
    <input type="hidden" id="char_id" name="char_id" value="{{ char_id }}">
    <input class="btn btn-primary" type="submit" value="&#10145; Lobby der Szene betreten!"/>
    </div>
    </form>

    **Countdown**
    
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
        try:
            countdown = event['countdown']
        except:
            countdown = ""

        try:
            char_id = event['char_id']
        except:
            char_id = ""
            
        print("char_id")
        print(char_id)
        

        if char_id != "":
            user_char_name = await self.db_get_char_id_char_name(char_id)    
            print("hole char name")
            print(user_char_name)
            
        else:
            user_char_name = ""
            print("hole char name nicht")
        
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
            
            if  slot_state == 1: # slot is used 
                char_name = await self.db_get_slot_char_name(slot_id)
                slot_template = slot_template.replace('**js_button_function**','free_the_slot')
                slot_template = slot_template.replace('**button_text**','Platz freigeben')

                if str(user_char_name) == str(char_name): # disable button not here, maybe on countdown
                    slot_template = slot_template.replace('**button_disabled**','**button_disabled_for_lvl2**')
                else: # disable button here now - because first you need to free the taken slot
                    slot_template = slot_template.replace('**button_disabled**','disabled')
                    
            else: # slot is free
                slot_template = slot_template.replace('**js_button_function**','take_the_slot')
                slot_template = slot_template.replace('**button_text**','Platz belegen')
                slot_template = slot_template.replace('**button_disabled**','**button_disabled_for_lvl2**')

            
            if char_name == False:
                char_name = ""
                    
            slot_template = slot_template.replace('**slot_id_char_name**',char_name)
                
            html = html + slot_template 
        
        html = html + self.html_table_bottom
        html = html.replace('\n','')
        
        ## add countdown if it is set:
        
        if countdown == "":
            countdown_html = '' # no countdown
        else: # countdown is running / game is ready
            countdown = int(countdown)
            if countdown < 11: 
                countdown = (countdown -11) * -1
                if countdown < 6:
                    html = html.replace('**button_disabled_for_lvl2**','disabled')
                else:
                    html = html.replace('**button_disabled_for_lvl2**','')
                    
                countdown_html = """
                <p style="color:green;">**seconds** Sekunden bis Spielstart!</p>
                """
                countdown_html = countdown_html.replace('**seconds**', str(countdown))
            else:
                countdown_html = """
                <p style="color:red;">Go!</p>
                """
        html = html + countdown_html 
        



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
        char_id = text_data_json['char_id']

        if message == 'heartbeat':
            # (TODO!) update timestamps, delete old entrys
            
            # check timestamps, delete old and zombie  entrys
           
            # check if all slots are taken
            req_players = await self.db_get_num_players()
            players_in_lobby = 0
            for slot in range(req_players):
                slot_state = await self.db_get_slot_state(slot)
                if slot_state == 1: # slot is used
                    players_in_lobby = players_in_lobby + 1
                    
            if req_players == players_in_lobby: # lobby is full 
                
                # create/check countdown
                # do all slots have the same timestamp in countdown?
                
                locked_in_datetimes = await self.db_get_list_datetime_locked_in(self.scene_id)
                last_timestamp = locked_in_datetimes[0]
                
                # singleplayer check and repair
                if last_timestamp is None and req_players == 1: 
                    last_timestamp = datetime.now()
                    
                timestamps_are_the_same = True
                
                for timestamp in locked_in_datetimes:
                    if last_timestamp != timestamp:
                        timestamps_are_the_same = False
                
                if timestamps_are_the_same:  # check if countdown is over
                    now = int(datetime.now().strftime('%s'))
                    
                    last_timestamp = int(last_timestamp.strftime('%s'))
                    timediff = now-last_timestamp
                    
                    if timediff > 0: # wait a second for updates...
                        await self.channel_layer.group_send(
                            self.msg_group_name, { 
                                                  'type': 'msg_group_send_content',  
                                                  'countdown' : str(timediff), 
                                                  'char_id' : char_id,
                                                  } 
                        )            
                    
                else:
                    set_datetimes = await self.db_set_datetime_locked_in()
                
            else:
                pass # lobby is not full
            
            # if yes, then replace slot table with form to join a scene, broadcast to all
            
        if message == 'free_the_slot':
            slot_id = text_data_json['slot_id']
            
            await self.db_free_slot(slot_id, char_id)
            
            await self.channel_layer.group_send(
                self.msg_group_name, { 'type': 'msg_group_send_content', 'char_id' : char_id,  } 
            )            
        
        if message == 'take_the_slot':
            slot_id = text_data_json['slot_id']
            
            await self.db_set_char_to_slot(slot_id, char_id)
                     
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
            return False

    @database_sync_to_async     
    def db_get_char_id_char_name(self, char_id):
        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        if LobbySlots.objects.filter(game_scene_id=self.scene_id, user_char_id=char_id).exists():
            char_id_name = LobbySlots.objects.filter(game_scene_id=self.scene_id, user_char_id=char_id)
            return char_id_name[0].user_char_id
        else:
            return ''

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

    @database_sync_to_async     
    def db_get_list_datetimes(self, slot_id):
        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        
        list_of_slot_entrys = LobbySlots.objects.filter(game_scene_id=self.scene_id).order_by('slot_id')
        
        locked_in = []
        slot_taken = []
        
        for row in list_of_slot_entrys:
            locked_in.append(row.datetime_locked_in)
            slot_taken.append(row.datetime_slot_taken)
            
        return (locked_in,slot_taken)


    @database_sync_to_async     
    def db_get_list_datetime_locked_in(self, slot_id):
        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        list_of_slot_entrys = LobbySlots.objects.filter(game_scene_id=self.scene_id).order_by('slot_id')
        locked_in = []
        
        for row in list_of_slot_entrys:
            locked_in.append(row.datetime_locked_in)
            
        return locked_in
    
    @database_sync_to_async     
    def db_set_datetime_locked_in(self):
        self.scene_id = self.scope['url_route']['kwargs']['scene_id']
        try:
            LobbySlots.objects.filter(game_scene_id=self.scene_id).update(datetime_locked_in=Now())
            return True
        except:
            return False
        


    

    pass