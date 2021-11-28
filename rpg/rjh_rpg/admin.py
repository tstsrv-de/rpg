from django.contrib import admin

# Register your models here.

from rjh_rpg.models import UserChar
from rjh_rpg.models import GameState, GameScenes, GameScenesRunning, GamesScenesSteps

admin.site.register(UserChar)
admin.site.register(GameState)
admin.site.register(GamesScenesSteps)
admin.site.register(GameScenesRunning)
admin.site.register(GameScenes)
