from rjh_rpg.models import Games
from channels.db import database_sync_to_async

@database_sync_to_async
def db_set_game_id_to_finished(game_id):
    return Games.objects.filter(id=game_id).update(game_finished=True)

@database_sync_to_async
def db_get_is_game_id_finished(game_id):
    return Games.objects.get(id=game_id).game_finished
    