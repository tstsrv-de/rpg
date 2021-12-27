import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string
from rjh_rpg.consumer_game_tools import db_set_game_id_to_finished
from rjh_rpg.consumer_game_tools import db_get_is_game_id_finished
from rjh_rpg.consumer_game_tools import db_get_game_log
from rjh_rpg.consumer_game_tools import db_expand_game_log
from rjh_rpg.consumer_game_tools import db_get_round_state, db_set_round_state
from rjh_rpg.consumer_game_tools import db_get_is_round_state_locked, db_set_round_state_locked
from rjh_rpg.consumer_game_tools import db_increase_round_counter

class Consumer(AsyncWebsocketConsumer):
    
    mycounter = 0
    
    # optimze traffic
    last_game_log_content = ""
    
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.msg_group_name = 'game-%s' % self.game_id

        await self.channel_layer.group_add(
            self.msg_group_name,
            self.channel_name
        )
        
        await self.accept()
                        
        



    async def msg_group_send_game_log_update(self, event):
        game_log_content = await db_get_game_log(self.game_id)
        
        if game_log_content == self.last_game_log_content:
            # skip sending if no update since last message
            pass
        else:
            await self.send(text_data=json.dumps({ 
                'game_msg_type': 'game_log_update',
                'game_websocket_content': str(game_log_content),
            }))
            self.last_game_log_content = game_log_content

    async def msg_group_send_counter_update(self, event):
        # only send a fresh value for the counter

        await self.send(text_data=json.dumps({ 
            'game_msg_type': 'game_counter_update',
            'game_websocket_content': str(self.mycounter),
        }))

    async def msg_group_send_endscreen(self, event):
        html = render_to_string('game_endscreen.html')

        await self.send(text_data=json.dumps({ 
            'game_msg_type': 'game_endscreen',
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
            
            self.mycounter = self.mycounter + 1
            print("alive, game-id: " + str(self.game_id) + " self_game_id: " + str(self.game_id) +  " and counter " + str(self.mycounter))

            # round state is used to run through the rounds, depending on their states
            round_state = await db_get_round_state(self.game_id)
            print ("current round_state: " + str(round_state))

            ''' # see doku, development 27.12.2021, essance is: 
            0 inital for new games
            100 enemy makes damage
            200 check user-chars with less than 0 hp, mark them as dead
            300 check if any user-chars are alive, if not end game with gameover-flag 990
            400 collect and save the next actions from all alive user-chars, proceed only every user-char has a next action set
            500 run the collected actions (make damage, use ability, pass turn), check after each user-char if enemy is alive, if not end game with win-flag 995
            600 increase round_counter + 1
            700 reset round_state to 100            
            '''                        

            if round_state == 0: 
                # switch up to first run of first round
                round_state_is_locked = await db_get_is_round_state_locked(self.game_id)
                if round_state_is_locked == True:
                    # do nothing, wait for others to finish and free round_state
                    pass
                else: 
                    # (TODO!) understand why this works only without await on the lock AND test it with more players (see if lock works at all!)
                    db_set_round_state_locked(self.game_id, True) 
                    await db_set_round_state(self.game_id, 100)
                    await db_increase_round_counter(self.game_id)
                    db_set_round_state_locked(self.game_id, False)
                    print ("round_state set to 100")

            elif round_state == 100:
                pass
            elif round_state == 200:
                pass
            elif round_state == 300:
                pass
            elif round_state == 400:
                pass
            elif round_state == 500:
                pass
            elif round_state == 600:
                pass
            elif round_state == 700:
                pass             
            else:
                # should not happen
                print("no round state on known rules")
                pass

            await self.channel_layer.group_send(self.msg_group_name, { 
                                'type': 'msg_group_send_game_log_update', })

            await self.channel_layer.group_send(self.msg_group_name, { 
                                'type': 'msg_group_send_counter_update', })


        if message == 'set_game_to_finished':
            set_game_to_finished = await db_set_game_id_to_finished(self.game_id)
            print("set game to finished, game-id: " + str(self.game_id) + " and its return value was: " + str(set_game_to_finished))
            await self.channel_layer.group_send(self.msg_group_name, { 
                                'type': 'msg_group_send_endscreen',  })


        if message == 'game_log_think':
            msg_to_add = text_data_json['msg_to_gamelog']
            print("Gamelog add: " + str(msg_to_add))
             
            text_to_add = "Spieler denkt .o0( " + str(msg_to_add) + " )<br />"
            await db_expand_game_log(self.game_id,text_to_add)
            
            
