from datetime import datetime
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
    
    
    def __str__(self):
        return self.name
    
    
class GameState(models.Model):   # wo ist der char? in der weltmap? oder in einer szene?
    
    char = models.ForeignKey(UserChar, on_delete=models.CASCADE, unique=True)
    place = models.IntegerField(default=0) # 0 = weltmap, n > 0 = laufende_game_id
    charLogin = models.DateTimeField(default=datetime.now) 
    char_user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.char)
    
    
class GamesScenesSteps(models.Model): # schritte der szenen
    name = models.CharField(max_length=100)
    #game_scene = 
    #parent_step = 
    #next_step = 
    #possible_actions = ('kampf','schritt vorwärts', )
    #background_image = 
    
class GameScenesRunning(models.Model): # das laufende spiel
    char = models.ForeignKey(UserChar, on_delete=models.CASCADE, unique=True)
    scene_step = models.ForeignKey(GamesScenesSteps, on_delete=models.CASCADE)
    game_id = models.BigIntegerField() # instanz id, 0= wartende spieler >=1 spiel läuft
        
class GameScenes(models.Model): # eigenschaften der szenen   // GAME OVER Screen? als step? 
    name = models.CharField(unique=True, max_length=300)
    start_step = models.ForeignKey(GamesScenesSteps, on_delete=models.CASCADE, unique=True)  # start step = lobby, end step = after game screen (fortschritt, belohnungen, ...)
    req_players = models.BigIntegerField(default=1) # anzahl notweniger spieler

