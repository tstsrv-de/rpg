from django.contrib import admin

# Register your models here.

from rjh_rpg.models import UserChar
from rjh_rpg.models import GameState

admin.site.register(UserChar)
admin.site.register(GameState)
