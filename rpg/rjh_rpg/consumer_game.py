import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string
from rjh_rpg.consumer_game_tools import db_set_game_id_to_finished
from rjh_rpg.consumer_game_tools import db_get_is_game_id_finished
from rjh_rpg.consumer_game_tools import db_get_game_log
from rjh_rpg.consumer_game_tools import db_expand_game_log
from rjh_rpg.consumer_game_tools import db_get_round_state, db_set_round_state
from rjh_rpg.consumer_game_tools import db_get_is_round_state_locked, db_set_round_state_locked
from rjh_rpg.consumer_game_tools import db_increase_round_counter, db_get_round_counter
from rjh_rpg.consumer_game_tools import db_get_enemy_name, db_get_enemy_ap
from rjh_rpg.consumer_game_tools import db_get_user_char_in_game_list, db_get_random_alive_user_char_in_games_id, db_give_dmg_to_user_char, db_get_char_name_of_user_char_in_games_id, db_get_died_but_not_dead_user_chars, db_set_user_char_to_dead

class Consumer(AsyncWebsocketConsumer):
    
    mycounter = 0
    round_state_token_is_mine = False
    
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
            700 reset round_state and loop to 100

            round-states without looping anymore:
            990 gaveover / game lost
            995 game is won
            '''                        

            # this part sadly does not work correctly. problem here is that with multiple 
            # clients/players, the rounds are driven at the same time. solution should be
            # a token -- but this token also need to be synced, which brings new promblems.
            # (TODO!) get expert help on that.

            self.round_state_token_is_mine = False
            if await db_get_is_round_state_locked(self.game_id) == False:
                db_set_round_state_locked(self.game_id, True) 
                self.round_state_token_is_mine = True     
                           
                
            if self.round_state_token_is_mine == True:
                if round_state == 0: 
                    # switch up to first run of first round
                        await db_set_round_state(self.game_id, 100)
                        await db_increase_round_counter(self.game_id)
                        print ("round_state set to 100")

                elif round_state == 100:
                    await db_expand_game_log(self.game_id, "<br /> ⏩ Es beginnt Runde " + str(await db_get_round_counter(self.game_id)) + ": <br /><br />")

                    char_to_hit = await db_get_random_alive_user_char_in_games_id(self.game_id)

                    if not char_to_hit: # failsave in case no player is alive
                        await db_set_round_state(self.game_id, 300)

                    else:
                        ap_to_deliver = await db_get_enemy_ap(self.game_id)
                        dmg_dealt = await db_give_dmg_to_user_char(char_to_hit, ap_to_deliver)
                        char_name_to_hit = await db_get_char_name_of_user_char_in_games_id(char_to_hit)

                        await db_expand_game_log(self.game_id, " ⚔ " + str(await db_get_enemy_name(self.game_id)) + " greift mit "+ str(ap_to_deliver) +" Angriffspunkten an...<br />" )

                        await db_expand_game_log(self.game_id, " 💥 ...und trifft " + char_name_to_hit + " für " + str(dmg_dealt[2]) + " Schaden. <br /> 💔 Die Lebenspunkte von " + char_name_to_hit + " sinken von " + str(dmg_dealt[0]) + " auf " + str(dmg_dealt[1]) + ". <br />")

                        await db_set_round_state(self.game_id, 200)    

                elif round_state == 200:
                    char_list = await db_get_user_char_in_game_list(self.game_id)
                    print("char_list: " + str(char_list))
                    new_dead_user_chars = await db_get_died_but_not_dead_user_chars(self.game_id)
                    print("new_dead_user_chars: " + str(new_dead_user_chars))
                    for user_char in new_dead_user_chars:
                        print("user_char dead: " + str(user_char))
                        await db_set_user_char_to_dead(user_char)
                        await db_expand_game_log(self.game_id, "<br /> 💀 " + str(await db_get_char_name_of_user_char_in_games_id(user_char)) + " ist gestorben! <br />" )

                    await db_set_round_state(self.game_id, 300)    


                elif round_state == 300:
                    at_least_one_player_alive = await db_get_random_alive_user_char_in_games_id(self.game_id)

                    if not at_least_one_player_alive: 
                        print("Gameover!")
                        await db_set_round_state(self.game_id, 995)
                        await db_expand_game_log(self.game_id, "<br /> 🪦 Kein Spieler hat überlebt.  <br /> 🥇 " + str(await db_get_enemy_name(self.game_id)) + " war siegreich. <br /> <br /> <br />")

                    else:
                        await db_set_round_state(self.game_id, 400)

                elif round_state == 400:
                    await db_set_round_state(self.game_id, 500)    
                elif round_state == 500:
                    await db_set_round_state(self.game_id, 600)    
                elif round_state == 600:
                    await db_increase_round_counter(self.game_id)
                    await db_set_round_state(self.game_id, 700)                
                elif round_state == 700:
                    await db_set_round_state(self.game_id, 100)                
                    
                elif round_state == 990:
                    pass
                    
                elif round_state == 995:                
                    pass
                                    
                else:
                    # should not happen
                    print("no round state on known rules")
                
                # release round-state-token
                print("round-state-token released")
                db_set_round_state_locked(self.game_id, False)
                self.round_state_token_is_mine = False

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
            
            
