from rjh_rpg.models import GameScenes, Games, UserCharInGames, UserChar, User, AbilitysToApply
from channels.db import database_sync_to_async
import random
from math import ceil
from rjh_rpg.rpg_tools import rpg_websocket_get_config, rpg_get_config

@database_sync_to_async
def db_set_game_id_to_finished(game_id):
    return Games.objects.filter(id=game_id).update(game_finished=True)

@database_sync_to_async
def db_get_is_game_id_finished(game_id):
    return Games.objects.get(id=game_id).game_finished


@database_sync_to_async
def db_get_game_log(game_id):
    return str(Games.objects.get(id=game_id).game_log)

@database_sync_to_async
def db_expand_game_log(game_id, text_to_add):
    game_obj = Games.objects.get(id=game_id)
    game_log_now = str(game_obj.game_log)
    game_log_new = game_log_now + str(text_to_add)
    game_obj.game_log = game_log_new
    game_obj.save()

@database_sync_to_async
def db_get_round_state(game_id):
    return Games.objects.get(id=game_id).round_state

@database_sync_to_async
def db_set_round_state(game_id, new_round_state):
    return Games.objects.filter(id=game_id).update(round_state=new_round_state)

@database_sync_to_async
def db_get_is_round_state_locked(game_id):
    return bool(Games.objects.get(id=game_id).round_state_locked)

@database_sync_to_async
def db_set_round_state_locked(game_id, new_round_state_locked):
    return Games.objects.filter(id=game_id).update(round_state=bool(new_round_state_locked))


@database_sync_to_async
def db_increase_round_counter(game_id):
    return Games.objects.filter(id=game_id).update(round_counter=(int(Games.objects.get(id=game_id).round_counter)+1))

@database_sync_to_async
def db_get_round_counter(game_id):
    return int(Games.objects.get(id=game_id).round_counter)


@database_sync_to_async
def db_get_enemy_name(game_id):
    game_scene_id = Games.objects.get(id=game_id).game_scene_id
    return str(GameScenes.objects.get(name=game_scene_id).enemy_name)

@database_sync_to_async
def db_get_enemy_current_ap(game_id):
    return int(Games.objects.get(id=game_id).enemy_current_ap)

@database_sync_to_async
def db_set_enemy_current_ap(game_id, new_ap):
    return Games.objects.filter(id=game_id).update(enemy_current_ap=new_ap)

@database_sync_to_async
def db_get_enemy_base_ap(game_id):
    game_scene_id = Games.objects.get(id=game_id).game_scene_id
    return int(GameScenes.objects.get(name=game_scene_id).enemy_ap)


@database_sync_to_async
def db_get_user_char_in_game_list(game_id):
    user_chars_in_game = UserCharInGames.objects.filter(game_id=game_id).order_by('id')
    user_char_in_game_list = [] 
    for user_char in user_chars_in_game:
        user_char_in_game_list.append(user_char.id)
    return user_char_in_game_list

@database_sync_to_async
def db_get_random_alive_user_char_in_games_id(game_id):
    try:
        alive_user_chars = UserCharInGames.objects.filter(game_id=game_id, current_hp__gte = 0, user_char_died=False)
        random_alive_user_char = random.choice(alive_user_chars)
        return random_alive_user_char.id
    except:
        return None

@database_sync_to_async
def db_get_died_but_not_dead_user_chars(game_id):
    fresh_died_user_chars = UserCharInGames.objects.filter(game_id=game_id, current_hp=0, user_char_died=False)
    new_deads = []
    for user_char in fresh_died_user_chars:
        new_deads.append(user_char.id)
    return new_deads

@database_sync_to_async
def db_get_alive_user_chars(game_id):
    fresh_died_user_chars = UserCharInGames.objects.filter(game_id=game_id, current_hp__gte=0, user_char_died=False).order_by('id')
    alive_user_chars = []
    for user_char in fresh_died_user_chars:
        alive_user_chars.append(user_char.id)
    return alive_user_chars

@database_sync_to_async
def db_set_user_char_to_dead(user_char_in_games_id):
    return UserCharInGames.objects.filter(id=user_char_in_games_id).update(user_char_died=True)


@database_sync_to_async
def db_give_dmg_to_user_char(user_char_in_games_id, ap_to_deliver):
    last_hp = UserCharInGames.objects.get(id=user_char_in_games_id).current_hp
    ap_to_deliver = random.randint(int(ap_to_deliver * rpg_get_config("dmg_min")), int(ap_to_deliver * rpg_get_config("dmg_max"))) 
    new_hp = last_hp - int(ap_to_deliver)
    if new_hp < 0:
        new_hp = 0
    UserCharInGames.objects.filter(id=user_char_in_games_id).update(current_hp=new_hp)
    dmg_taken = last_hp - new_hp
    return (last_hp, new_hp, dmg_taken)
    
@database_sync_to_async
def db_get_char_name_of_user_char_in_games_id(user_char_in_games_id):
    char_name = UserCharInGames.objects.get(id=user_char_in_games_id).user_char_id
    return str(char_name)

@database_sync_to_async
def db_get_user_char_from_user_id(game_id, user_id):
    this_users_user_chars = []
    for user_char in UserChar.objects.filter(usernickname=user_id):
        this_users_user_chars.append(user_char.name)
    
    for user_char_in_game_id in UserCharInGames.objects.filter(game_id=game_id):
        for user_char_of_this_user in this_users_user_chars:
            if str(user_char_of_this_user) == str(user_char_in_game_id.user_char_id):
                return user_char_in_game_id.user_char_id

    return None

@database_sync_to_async
def db_get_first_user_char_of_game_id(game_id):
    first_user_char_of_game = UserCharInGames.objects.filter(game_id=game_id).order_by('id')
    return str(first_user_char_of_game[0].user_char_id)

@database_sync_to_async
def db_set_next_user_char_action(user_char_in_games_id, action_type):
    return UserCharInGames.objects.filter(id=user_char_in_games_id).update(next_action=action_type)

@database_sync_to_async
def db_get_user_chars_next_action(user_char_in_games_id):
    return str(UserCharInGames.objects.get(id=user_char_in_games_id).next_action)

@database_sync_to_async
def db_get_user_chars_with_no_next_action(game_id):
    undecided = UserCharInGames.objects.filter(game_id=game_id, user_char_died=False, next_action='')
    undecided_to_remind = []
    for user_char in undecided:
        undecided_to_remind.append(user_char.id)
    return undecided_to_remind

@database_sync_to_async
def db_reset_all_next_user_char_actions(game_id):
    return UserCharInGames.objects.filter(game_id=game_id).update(next_action='', next_action_was_reminded=False)

@database_sync_to_async
def db_get_user_chars_next_action_was_reminded(user_char_in_games_id):
    return bool(UserCharInGames.objects.get(id=user_char_in_games_id).next_action_was_reminded)

@database_sync_to_async
def db_set_next_user_char_action_was_reminded(user_char_in_games_id):
    return UserCharInGames.objects.filter(id=user_char_in_games_id).update(next_action_was_reminded=True)


@database_sync_to_async
def db_get_user_char_current_ap(user_char_in_games_id):
    return UserCharInGames.objects.get(id=user_char_in_games_id).current_ap

@database_sync_to_async
def db_get_user_char_base_ap(user_char_in_games_id):
    user_char_in_games_id = UserCharInGames.objects.get(id=user_char_in_games_id).user_char_id.id
    base_ap = UserChar.objects.get(id=user_char_in_games_id).ap
    return int(base_ap)

@database_sync_to_async
def db_set_user_char_current_ap(user_char_in_games_id, new_ap):
    return UserCharInGames.objects.filter(id=user_char_in_games_id).update(current_ap=new_ap)

@database_sync_to_async
def db_get_user_char_base_hp(user_char_in_games_id):
    user_char_in_games_id = UserCharInGames.objects.get(id=user_char_in_games_id).user_char_id.id
    base_hp = UserChar.objects.get(id=user_char_in_games_id).hp
    return int(base_hp)

@database_sync_to_async
def db_set_user_char_current_hp(user_char_in_games_id, new_hp):
    return UserCharInGames.objects.filter(id=user_char_in_games_id).update(current_hp=new_hp)

@database_sync_to_async
def db_get_user_char_current_hp(user_char_in_games_id):
    return UserCharInGames.objects.get(id=user_char_in_games_id).current_hp



@database_sync_to_async
def db_give_dmg_to_enemy(game_id, ap_to_deliver):
    last_hp = Games.objects.get(id=game_id).enemy_current_hp
    ap_to_deliver = random.randint(int(ap_to_deliver * rpg_get_config("dmg_min")), int(ap_to_deliver * rpg_get_config("dmg_max"))) 
    new_hp = last_hp - int(ap_to_deliver)
    if new_hp < 0:
        new_hp = 0
    dmg_taken = last_hp - new_hp
    Games.objects.filter(id=game_id).update(enemy_current_hp=new_hp)
    return (last_hp, new_hp, dmg_taken)

@database_sync_to_async
def db_get_end_msg_shown(game_id):
    return bool(Games.objects.get(id=game_id).game_end_msg_shown)

@database_sync_to_async
def db_set_end_msg_to_shown(game_id):
    return Games.objects.filter(id=game_id).update(game_end_msg_shown=True)


@database_sync_to_async
def db_give_xp_to_user_char(user_char_in_games_id, xp_to_give):
    # factor to slow char progress down
    xp = ceil(xp_to_give * rpg_get_config("xp_to_give_factor"))
    last_game_xp = UserCharInGames.objects.get(id=user_char_in_games_id).user_chars_xp_of_this_game_id
    new_game_xp = last_game_xp + int(xp)
    update_game_xp = UserCharInGames.objects.filter(id=user_char_in_games_id).update(user_chars_xp_of_this_game_id=new_game_xp)

    user_char_id = UserCharInGames.objects.get(id=user_char_in_games_id).user_char_id.id
    last_char_xp = UserChar.objects.get(id=user_char_id).xp_to_spend
    new_char_xp = last_char_xp + int(xp)
    update_char_xp = UserChar.objects.filter(id=user_char_id).update(xp_to_spend=new_char_xp)
    
    return update_char_xp + update_game_xp

@database_sync_to_async
def db_get_user_char_this_game_xp(user_char_in_games_id):
    return int(UserCharInGames.objects.get(id=user_char_in_games_id).user_chars_xp_of_this_game_id)

@database_sync_to_async
def db_give_bonus_xp_to_user_char(user_char_in_games_id, xp):

    user_char_id = UserCharInGames.objects.get(id=user_char_in_games_id).user_char_id.id
    last_char_xp = UserChar.objects.get(id=user_char_id).xp_to_spend
    new_char_xp = last_char_xp + int(xp)
    update_char_xp = UserChar.objects.filter(id=user_char_id).update(xp_to_spend=new_char_xp)
    
    return update_char_xp


@database_sync_to_async
def db_get_abiliy_of_user_char(user_char_in_games_id):
    user_char_id = UserCharInGames.objects.get(id=user_char_in_games_id).user_char_id.id
    abiliy_of_user_char = UserChar.objects.get(id=user_char_id).Klasse
    return str(abiliy_of_user_char)

@database_sync_to_async
def db_add_abiliy_of_user_char_to_round(game_id, user_char_in_games_id, round_number):
    ability_to_add = AbilitysToApply()
    ability_to_add.game_id = Games.objects.get(id=game_id)
    ability_to_add.user_char_id = UserCharInGames.objects.get(id=user_char_in_games_id)
    ability_to_add.round_number = round_number
    ability_to_add.ability_was_applyed = False
    return ability_to_add.save()

@database_sync_to_async
def db_get_next_not_applied_abiliy_of_round(game_id, round_number):
    try:
        next_user_char_in_games_id = AbilitysToApply.objects.filter(game_id=game_id, round_number=round_number, ability_was_applyed=False)
        return (next_user_char_in_games_id[0].id, next_user_char_in_games_id[0].user_char_id)
    except:
        return None

@database_sync_to_async
def db_set_next_action_to_apply_to_done(next_action_id):
    return AbilitysToApply.objects.filter(id=next_action_id).update(ability_was_applyed=True)    


@database_sync_to_async
def db_get_win_text(game_id):
    game_scene_id = Games.objects.get(id=game_id).game_scene_id
    return str(GameScenes.objects.get(name=game_scene_id).win_text)

@database_sync_to_async
def db_get_gameover_text(game_id):
    game_scene_id = Games.objects.get(id=game_id).game_scene_id
    return str(GameScenes.objects.get(name=game_scene_id).gameover_text)
