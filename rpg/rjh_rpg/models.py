from datetime import datetime
from typing_extensions import Required
from django.db import models

# Create your models here.

from django.conf import settings
from django.utils.translation import gettext_lazy

class User(models.Model):
    nickname = models.CharField(unique=True,max_length=100)
    email = models.EmailField(unique=True)
    text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nickname
    
    
class UserChar(models.Model):
    
    class CharSex(models.TextChoices):
        FEMALE = 'F', gettext_lazy('Frauchen')
        MALE = 'M', gettext_lazy('Männchen')
        NONE = '0', gettext_lazy('Keins')

    usernickname = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(unique=True,max_length=100)
    birthplace = models.CharField(max_length=200, null=True, blank=True)

    char_sex = models.CharField(
            max_length=1,
            choices=CharSex.choices,
            default=CharSex.NONE,
        )

    def __str__(self): # (TODO!) this maybe the cause of many problems... why do we need this? would it be better w/o? to fetch id's...
        return self.name

class GamesScenesSteps(models.Model): # schritte der szenen
    name = models.CharField(max_length=100)
    #game_scene = 
    #parent_step = 
    #next_step = 
    #possible_actions = ('kampf','schritt vorwärts', )
    #background_image = 

class GameScenes(models.Model): # eigenschaften der szenen   // GAME OVER Screen? als step? 
    name = models.CharField(unique=True, max_length=300)
    start_step = models.ForeignKey(GamesScenesSteps, on_delete=models.CASCADE, unique=True)  # start step = lobby, end step = after game screen (fortschritt, belohnungen, ...)
    req_players = models.BigIntegerField(default=1) # anzahl notweniger spieler
    
    def __str__(self):
        return self.name    


class LobbySlots(models.Model):
    user_char_id = models.ForeignKey(UserChar, on_delete=models.CASCADE, unique=True)
    game_scene_id = models.ForeignKey(GameScenes, on_delete=models.CASCADE) # also known as scene_id
    slot_id = models.IntegerField(null=True, blank=True) # also known as scene_id    (TODO!) install as a required field w/o null and blank   
    datetime_slot_taken = models.DateTimeField(default=datetime.now) 
    datetime_locked_in = models.DateTimeField(null=True, blank=True)    


 # better name would have been 'UserCharState'
 # since there is no information about the games - only of the user and its char
class GameState(models.Model): 
    char = models.ForeignKey(UserChar, on_delete=models.CASCADE, unique=True)
    place = models.IntegerField(default=0) # 0 = weltmap, n > 0 = laufende_game_id
    charLogin = models.DateTimeField(default=datetime.now) 
    char_user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.char)
    

class HelperCounter(models.Model):
    name = models.CharField(unique=True, max_length=300)
    count = models.BigIntegerField(default=0)
    last_update = models.DateTimeField(default=datetime.now) 
    
