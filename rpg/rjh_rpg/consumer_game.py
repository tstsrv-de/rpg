from datetime import datetime
from math import ceil
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
from rjh_rpg.consumer_game_tools import db_get_enemy_name, db_get_enemy_current_ap, db_set_enemy_current_ap
from rjh_rpg.consumer_game_tools import db_get_user_char_in_game_list, db_get_random_alive_user_char_in_games_id, db_give_dmg_to_user_char, db_get_char_name_of_user_char_in_games_id, db_get_died_but_not_dead_user_chars, db_set_user_char_to_dead, db_get_user_char_from_user_id, db_get_first_user_char_of_game_id, db_get_alive_user_chars
from rjh_rpg.consumer_game_tools import db_set_next_user_char_action, db_get_user_chars_next_action, db_get_user_chars_with_no_next_action, db_reset_all_next_user_char_actions, db_set_next_user_char_action_was_reminded, db_get_user_chars_next_action_was_reminded
from rjh_rpg.consumer_game_tools import db_get_user_char_current_ap, db_give_dmg_to_enemy
from rjh_rpg.consumer_game_tools import db_get_end_msg_shown, db_set_end_msg_to_shown
from rjh_rpg.consumer_game_tools import db_give_xp_to_user_char, db_get_user_char_this_game_xp, db_give_bonus_xp_to_user_char
from rjh_rpg.consumer_game_tools import db_get_abiliy_of_user_char, db_add_abiliy_of_user_char_to_round, db_get_next_not_applied_abiliy_of_round, db_set_next_action_to_apply_to_done
from rjh_rpg.consumer_game_tools import db_get_enemy_base_ap, db_get_user_char_base_ap, db_get_user_char_base_hp, db_set_user_char_current_hp, db_set_user_char_current_ap, db_get_user_char_current_hp

class Consumer(AsyncWebsocketConsumer):

    mycounter = 0
    round_state_token_is_mine = False

    my_user_char = ""
    request_user_id = ""
    
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

        # save next action, but only if the round-state is 400 (collecting actions)
        if message == 'save_game_action' and await db_get_round_state(self.game_id) == 400:
            action_type = text_data_json['action_type']
            user_char_in_games_id = text_data_json['user_char_in_games_id']

            # only update if no choice has been made
            if await db_get_user_chars_next_action(user_char_in_games_id) == '':
                save_return = await db_set_next_user_char_action(user_char_in_games_id, action_type)
                action_string = ""
                if action_type == "attack":
                    action_string = "angreifen"
                elif action_type == "pass":
                    action_string = "aussetzen"
                elif action_type == "ability":
                    action_string = "seine Spezialfähigkeit einsetzen"

                if save_return == 1:
                    await db_expand_game_log(self.game_id, "<br /> ✅ " + str(await db_get_char_name_of_user_char_in_games_id(user_char_in_games_id)) + " wird gleich " + action_string + "!" )
            else:
                await db_expand_game_log(self.game_id, "<br /> ⏳ " + str(await db_get_char_name_of_user_char_in_games_id(user_char_in_games_id)) + " ist ungeduldig und würde gerne weitermachen..." )


        if message == 'alive':
            if self.request_user_id == "":
                self.request_user_id = text_data_json['request_user_id']
                self.my_user_char = await db_get_user_char_from_user_id(self.game_id, self.request_user_id)


            # (TODO!) update timestamps, delete old entrys
            # check timestamps, delete old and zombie  entrys
            
            self.mycounter = self.mycounter + 1
            print("alive, game-id: " + str(self.game_id) + " self_game_id: " + str(self.game_id) +  " and counter " + str(self.mycounter))

            # round state is used to run through the rounds, depending on their states
            round_state = await db_get_round_state(self.game_id)
            print ("current round_state: " + str(round_state))

            ''' # see doku, development 27.12.2021, essance is: 
            0 inital for new games
             50 apply effects of used abilitys
            100 enemy makes damage
            200 check user-chars with less than 0 hp, mark them as dead
            300 check if any user-chars are alive, if not end game with gameover-flag 990
            400 collect and save the next actions from all alive user-chars, proceed only every user-char has a next action set
            500 run the collected actions (make damage, use ability, pass turn), check after each user-char if enemy is alive, if not end game with win-flag 995
            600 increase round_counter + 1
            700 reset round_state and loop to 50

            round-states without looping anymore:
            990 gaveover / game lost
            995 game is won
            999 show link to exit
            '''

            # 2021-12-29 16:57 haenno:
            # this part sadly does not work correctly. problem here is that with multiple 
            # clients/players, the rounds are driven at the same time. solution should be
            # a token -- but this token also need to be synced, which brings new promblems.
            # (TODO!) get expert help on that.

            # self.round_state_token_is_mine = False
            # if await db_get_is_round_state_locked(self.game_id) == False:            
            #    db_set_round_state_locked(self.game_id, True) 
            #    self.round_state_token_is_mine = True     

            # 2021-12-29 16:57 haenno:
            # workaround: only the first user of all the users in the game will drive the rounds

            self.round_state_token_is_mine = False
            if str(self.my_user_char) == await db_get_first_user_char_of_game_id(self.game_id):
                db_set_round_state_locked(self.game_id, True) # take round-state-token
                self.round_state_token_is_mine = True
                print(str(self.my_user_char) + " is the first user of the game and drives the round! (TOKEN)")
            else:
                print(str(self.my_user_char) + " is not the first user of the game and has to wait. (NO TOKEN)")



            if self.round_state_token_is_mine == True:
                enemy_name = await db_get_enemy_name(self.game_id)
                current_round = await db_get_round_counter(self.game_id)
                if round_state == 0: 
                    # switch up to first run of first round and give 1 xp for gamestart to everyone
                    for user_char in await db_get_alive_user_chars(self.game_id):
                        await db_give_xp_to_user_char(user_char, 1)

                    await db_set_round_state(self.game_id, 100)
                    await db_increase_round_counter(self.game_id)


                # 50 apply all effects of used abilitys for this round
                elif round_state == 50:
                    await db_expand_game_log(self.game_id, "<br /> ⏩ Es beginnt Runde " + str(await db_get_round_counter(self.game_id)) + ": <br /><br />")

                    enemy_base_ap = await db_get_enemy_base_ap(self.game_id)
                    await db_set_enemy_current_ap(self.game_id, enemy_base_ap)
                    
                    reset_alive_user_chars_ap = await db_get_alive_user_chars(self.game_id)
                    for user_char in reset_alive_user_chars_ap:
                        this_user_char_base_ap = await db_get_user_char_base_ap(user_char)
                        await db_set_user_char_current_ap(user_char, this_user_char_base_ap)

                    proceed = False
                    while not proceed:
                        next_action_to_apply = await db_get_next_not_applied_abiliy_of_round(self.game_id, current_round)

                        if not next_action_to_apply: 
                            proceed = True
                            break
                        else:
                            ability_to_apply = await db_get_abiliy_of_user_char(next_action_to_apply[1].id)
                            user_char_name =         await db_get_char_name_of_user_char_in_games_id(next_action_to_apply[1].id)
                            
                            # Warrior = block damage
                            if ability_to_apply == "W":
                                await db_expand_game_log(self.game_id, " 🍬 Ein Effekt von " + user_char_name + " wirkt: " + enemy_name + " wird in dieser Runde 10% weniger Angriffspunkte haben... <br /> ")

                                enemy_current_ap = await db_get_enemy_current_ap(self.game_id)
                                new_ennemy_ap = enemy_current_ap - ceil(enemy_base_ap * 0.1)
                                if new_ennemy_ap < 1:
                                    new_ennemy_ap = 1
                                await db_set_enemy_current_ap(self.game_id, new_ennemy_ap)
                                await db_expand_game_log(self.game_id, " 🍬 ... " + enemy_name + " hat damit in dieser Runde nur noch " + str(new_ennemy_ap) + " Angriffspunkte! <br /> ")

                            # Priest = heal
                            elif ability_to_apply == "P":
                                await db_expand_game_log(self.game_id, " 💚 Ein Effekt von " + user_char_name + " wirkt: Die Spieler werden in dieser um 20% Ihrer Lebenspunkte geheilt... <br /> ")
                                
                                alive_user_chars = await db_get_alive_user_chars(self.game_id)
                                for user_char in alive_user_chars:
                                    this_user_char_base_hp = await db_get_user_char_base_hp(user_char)
                                    this_user_char_current_hp = await db_get_user_char_current_hp(user_char)
                                    this_user_char_name = await db_get_char_name_of_user_char_in_games_id(user_char)
                                    heal = ceil(this_user_char_base_hp * 0.1)                                    
                                    new_hp = this_user_char_current_hp + heal
                                    if new_hp > this_user_char_base_hp:
                                        new_hp = this_user_char_base_hp
                                        await db_expand_game_log(self.game_id, " 💚 ..." + this_user_char_name + " hatte bereits volle Lebenspunkte! <br />")
                                    else:
                                        await db_expand_game_log(self.game_id, " 💚 ..." + this_user_char_name + " erhält " + str(heal) + " Lebenspunkte und hat jetzt wieder " + str(new_hp) + " Lebenspunkte! <br />")
                                        await db_set_user_char_current_hp(user_char, new_hp)

                            # Mage = boost group damage
                            elif ability_to_apply == "M":
                                await db_expand_game_log(self.game_id, " 🚀 Ein Effekt von " + user_char_name + " wirkt: Alle Spieler werden in dieser Runde 10% mehr Angriffspunkte haben... <br /> ")

                                alive_user_chars = await db_get_alive_user_chars(self.game_id)
                                for user_char in alive_user_chars:
                                    this_user_char_base_ap = await db_get_user_char_base_ap(user_char)
                                    this_user_char_current_ap = await db_get_user_char_current_ap(user_char)
                                    this_user_char_name = await db_get_char_name_of_user_char_in_games_id(user_char)
                                    damage_boost = ceil(this_user_char_base_ap * 0.1)                                    
                                    new_ap = this_user_char_current_ap + damage_boost
                                    await db_set_user_char_current_ap(user_char, new_ap)
                                    await db_expand_game_log(self.game_id, " 🚀 ... " + this_user_char_name + " hat damit in dieser Runde " + str(new_ap) + " Angriffspunkte! <br /> ")

                            await db_expand_game_log(self.game_id, "<br />")
                            await db_set_next_action_to_apply_to_done(next_action_to_apply[0])
                    await db_set_round_state(self.game_id, 100)



                elif round_state == 100:

                    # (TODO!) Implement selection based on aggro-table instand of random char
                    char_to_hit = await db_get_random_alive_user_char_in_games_id(self.game_id) 

                    if not char_to_hit: # failsave in case no player is alive
                        await db_set_round_state(self.game_id, 300)

                    else:
                        ap_to_deliver = await db_get_enemy_current_ap(self.game_id)
                        dmg_dealt = await db_give_dmg_to_user_char(char_to_hit, ap_to_deliver)
                        char_name_to_hit = await db_get_char_name_of_user_char_in_games_id(char_to_hit)

                        await db_expand_game_log(self.game_id, " ⚔ " + enemy_name + " greift mit "+ str(ap_to_deliver) +" Angriffspunkten an...<br />" )

                        await db_expand_game_log(self.game_id, " 💥 ...und trifft " + char_name_to_hit + " für " + str(dmg_dealt[2]) + " Schaden. <br /> 💔 Die Lebenspunkte von " + char_name_to_hit + " sinken von " + str(dmg_dealt[0]) + " auf " + str(dmg_dealt[1]) + ". <br />")

                        await db_set_round_state(self.game_id, 200)


                elif round_state == 200:
                    new_dead_user_chars = await db_get_died_but_not_dead_user_chars(self.game_id)
                    for user_char in new_dead_user_chars:
                        await db_set_user_char_to_dead(user_char)
                        await db_expand_game_log(self.game_id, "<br /> 💀 " + str(await db_get_char_name_of_user_char_in_games_id(user_char)) + " ist gestorben! <br />" )

                    await db_set_round_state(self.game_id, 300)


                elif round_state == 300:
                    at_least_one_player_alive = await db_get_random_alive_user_char_in_games_id(self.game_id)

                    # the game is lost!
                    if not at_least_one_player_alive: 
                        await db_set_round_state(self.game_id, 990)

                    else:
                        await db_set_round_state(self.game_id, 400)


                elif round_state == 400: # collect and save next actions, see also msg_type 'save_action'
                    
                    proceed = True
                    for user_char in await db_get_user_chars_with_no_next_action(self.game_id):
                        if await db_get_user_chars_next_action_was_reminded(user_char) == False:
                            await db_expand_game_log(self.game_id, "<br /> ❓ " + str(await db_get_char_name_of_user_char_in_games_id(user_char)) + " überlegt konzentriert seinen nächsten Schritt... " )
                            await db_set_next_user_char_action_was_reminded(user_char)
                        proceed = False
                    
                    if proceed == True:
                        await db_expand_game_log(self.game_id, "<br />")
                        await db_set_round_state(self.game_id, 500)


                elif round_state == 500: # run the collected actions
                    
                    alive_user_chars = await db_get_alive_user_chars(self.game_id)
                    enemy_last_hp = ""
                    for user_char in alive_user_chars:
                        next_action = await db_get_user_chars_next_action(user_char)

                        if next_action == "pass":
                            await db_expand_game_log(self.game_id, "<br /> 😴 " + str(await db_get_char_name_of_user_char_in_games_id(user_char)) + " ist an der Reihe, schaut aber nur verlegen nach unten...  <br />" )

                        elif next_action == "attack":
                            user_char_ap = await db_get_user_char_current_ap(user_char)
                            await db_expand_game_log(self.game_id, "<br /> 🥊 " + str(await db_get_char_name_of_user_char_in_games_id(user_char)) + " greift " + enemy_name + " mit " + str(user_char_ap) + "  Angriffspunkten an...  <br />" )
                            
                            dmg_dealt = await db_give_dmg_to_enemy(self.game_id, user_char_ap)
                            
                            await db_expand_game_log(self.game_id, " 💥 ...und trifft " + enemy_name + " für " + str(dmg_dealt[2]) + " Schaden. <br /> 💔 Die Lebenspunkte von " + enemy_name + " sinken von " + str(dmg_dealt[0]) + " auf " + str(dmg_dealt[1]) + ". <br />")
                            
                            await db_give_xp_to_user_char(user_char, dmg_dealt[2])
                            
                            enemy_last_hp = dmg_dealt[1]
                            if enemy_last_hp == 0:
                                break
                            
                        elif next_action == "ability":
                            await db_expand_game_log(self.game_id, "<br /> 🎁 " + str(await db_get_char_name_of_user_char_in_games_id(user_char)) + " ist an der Reihe und bereitet seine Spezialfähigkeit vor...  <br />" )
                            await db_give_xp_to_user_char(user_char, await db_get_user_char_base_ap(user_char))
                            
                            '''
                            W -> warrior: reduce ap of enemy: next 3 rounds 10% less ap
                            M -> mage: increase ap of group: next 3 rounds 10% more ap
                            P -> priest: increase hp of group: next 2 rounds 20% more hp
                            '''
                            ability = await db_get_abiliy_of_user_char(user_char)

                            if ability == "W":
                                await db_expand_game_log(self.game_id, " 🎁 ..." + enemy_name + " wird in den nächsten 3 Runden jeweils 10% weniger Angriffspunkte haben! <br /> ")
                                await db_add_abiliy_of_user_char_to_round(self.game_id, user_char, current_round+1)
                                await db_add_abiliy_of_user_char_to_round(self.game_id, user_char, current_round+2)
                                await db_add_abiliy_of_user_char_to_round(self.game_id, user_char, current_round+3)

                            elif ability == "P":
                                await db_expand_game_log(self.game_id, " 🎁 ... die Gruppe wird in den nächsten 2 Runden um 20% Ihrer Lebenspunkte geheilt! <br /> ")
                                await db_add_abiliy_of_user_char_to_round(self.game_id, user_char, current_round+1)
                                await db_add_abiliy_of_user_char_to_round(self.game_id, user_char, current_round+2)

                            elif ability == "M":
                                await db_expand_game_log(self.game_id, " 🎁 ... die Gruppe wird in den nächsten 3 Runden jeweils 10% mehr Angriffspunkte haben! <br /> ")
                                await db_add_abiliy_of_user_char_to_round(self.game_id, user_char, current_round+1)
                                await db_add_abiliy_of_user_char_to_round(self.game_id, user_char, current_round+2)
                                await db_add_abiliy_of_user_char_to_round(self.game_id, user_char, current_round+3)

                    # enemy dead? then --> win, else: proceed
                    if enemy_last_hp == 0 and enemy_last_hp != "":
                        await db_set_round_state(self.game_id, 995)
                    else:
                        await db_set_round_state(self.game_id, 600)    


                elif round_state == 600:
                    await db_increase_round_counter(self.game_id)
                    await db_reset_all_next_user_char_actions(self.game_id)
                    await db_set_round_state(self.game_id, 700)                


                elif round_state == 700:
                    await db_set_round_state(self.game_id, 50)                
                    

                elif round_state == 990:
                    print("game ends - gameover!")            
                    await db_expand_game_log(self.game_id, "<br /> 🪦 Kein Spieler hat überlebt.  <br /> 🥇 " + enemy_name + " war siegreich. ")

                    await db_expand_game_log(self.game_id, "<br /><br /> 💰 Trotzdem gab es Erfahrungspunkte:")
                    
                    char_list = await db_get_user_char_in_game_list(self.game_id)
                    for user_char in char_list:
                        xp_earned = await db_get_user_char_this_game_xp(user_char)
                        await db_expand_game_log(self.game_id, "<br />     ➡️ " + str(await db_get_char_name_of_user_char_in_games_id(user_char)) + ": " + str(xp_earned) + " XP")
                    
                    await db_set_round_state(self.game_id, 999)




                elif round_state == 995:    
                    print("game ends - win!")

                    await db_expand_game_log(self.game_id, "<br /> 👏 " + enemy_name + " wurde besiegt! 🥳 🎉 🎊 🪅 🍻 ")
                    await db_set_round_state(self.game_id, 999)

                    await db_expand_game_log(self.game_id, "<br /><br /> 💰💰💰 Dafür gibt es Erfahrungspunkte mit Bonus:")
                    
                    total_xp_of_game = 0
                    
                    char_list = await db_get_user_char_in_game_list(self.game_id)
                    for user_char in char_list:
                        xp_earned = await db_get_user_char_this_game_xp(user_char)
                        total_xp_of_game = total_xp_of_game + xp_earned
                        print("total_xp_of_game:" + str(total_xp_of_game))

                    for user_char in char_list:
                        xp_earned = await db_get_user_char_this_game_xp(user_char)
                        await db_give_bonus_xp_to_user_char(user_char, (total_xp_of_game*2))
                        
                        await db_expand_game_log(self.game_id, "<br />     ➡️ " + str(await db_get_char_name_of_user_char_in_games_id(user_char)) + ": " + str(xp_earned) + " XP plus " + str(total_xp_of_game*2) + " XP Bonus!")




                elif round_state == 999:
                    print("show endscreen!")
                    if await db_get_end_msg_shown(self.game_id) == True: 
                        pass
                    else:
                        await db_set_end_msg_to_shown(self.game_id)
                        close_button = """<input type="submit" value="Spiel abschließen" onclick="set_game_to_finished();" style="background:#ffffff;  color: #000000; "" >"""
                        await db_expand_game_log(self.game_id,"<br /><br />Bitte schließt das Spiel nun ab: " + close_button)


                else:
                    # should not happen
                    print("no round state on known rules")
                
                db_set_round_state_locked(self.game_id, False) # release round-state-token
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


        if message == 'game_chat_msg':
            msg_to_add = text_data_json['msg_to_gamelog']
            if msg_to_add != "": 
                user_id = text_data_json['user_id'] 
                await db_expand_game_log(self.game_id, "<br /> 💬 " + str(await db_get_user_char_from_user_id(self.game_id, user_id)) + " sagt: \"" + str(msg_to_add) + "\"." )
                print("Gamelog add: " + str(msg_to_add))  
 
