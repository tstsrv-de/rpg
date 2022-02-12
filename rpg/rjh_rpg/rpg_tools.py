from rjh_rpg.models import UserCharInGames
from rjh_rpg.models import UserChar
from rjh_rpg.models import User
from rjh_rpg.models import GameState
from rjh_rpg.models import UserCharInGames
from rjh_rpg.models import Games
from rjh_rpg.models import MyRpgConfig
from channels.db import database_sync_to_async
from django.db.models.functions import Now


def rpg_user_is_player_of_this_game_id(game_id, request_user):

    user_is_player_of_this_game = False
    user_chars_in_game = UserCharInGames.objects.filter(game_id=game_id)
    for user_char in user_chars_in_game:
        # get user id based on userChar
        user_char_obj = UserChar.objects.get(id=user_char.user_char_id.id)
        if user_char_obj.usernickname == request_user:
            user_is_player_of_this_game = True

    return user_is_player_of_this_game


def rpg_user_has_active_game(request_user):
    
    for user_char in rpg_all_chars_from_user(request_user):
        for game_id in rpg_get_game_ids_to_user_char(user_char):
            game_id_is_finished = rpg_game_id_is_finished(game_id.id)
            if not game_id_is_finished: # means it is still running
                return int(game_id.id)

    return 0


def rpg_all_chars_from_user(request_user):
    char_list = []
    char_list_objects = UserChar.objects.filter(usernickname=request_user).order_by('name')

    for user_char in char_list_objects:
        char_list.append(user_char.name)

    return char_list

def rpg_get_game_ids_to_user_char(user_char):
    
    game_ids = []
    game_objects = UserCharInGames.objects.filter(user_char_id=rpg_user_char_name_to_id(user_char))

    for game in game_objects:
        game_ids.append(game.game_id)

    return game_ids

def rpg_user_char_id_to_name(user_char_id):
    return UserChar.objects.get(id=user_char_id).name

def rpg_user_char_name_to_id(user_char_name):
    return UserChar.objects.get(name=user_char_name).id

def rpg_game_id_is_finished(game_id):
    return Games.objects.get(id=game_id).game_finished
    
def rpg_get_config(config_to_get):

    try: 
        config_type = MyRpgConfig.objects.get(name=config_to_get).type
    
        if config_type == "int":
            return int(MyRpgConfig.objects.get(name=config_to_get).value)

        elif config_type == "str":
            return str(MyRpgConfig.objects.get(name=config_to_get).value)

        elif config_type == "float":
            return float(MyRpgConfig.objects.get(name=config_to_get).value)

        else:
            return None
    except:
        return None

@database_sync_to_async
def rpg_websocket_get_config(config_to_get):
    return rpg_get_config(config_to_get)

def rpg_user_char_chat_heartbeat(char_id):
    # last_chat_heartbeat
    try:
        print("Chat-Heartbeat from 'Char_ID':" + str(char_id))
        GameState.objects.filter(char=char_id).update(last_chat_heartbeat=Now())
    except:
        return None


@database_sync_to_async
def rpg_websocket_user_char_chat_heartbeat(char_id):    
    return rpg_user_char_chat_heartbeat(char_id)
