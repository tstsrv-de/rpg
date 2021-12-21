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

