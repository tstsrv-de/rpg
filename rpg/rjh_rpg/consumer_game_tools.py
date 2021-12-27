from rjh_rpg.models import Games
from channels.db import database_sync_to_async

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
    current_round_state = Games.objects.get(id=game_id).round_state
    return current_round_state

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

