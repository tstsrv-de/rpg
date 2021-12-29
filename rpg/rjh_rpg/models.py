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
        FEMALE = 'F', gettext_lazy('Frau')
        MALE = 'M', gettext_lazy('Mann')

    usernickname = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(unique=True,max_length=100)
    Geburtsort = models.CharField(max_length=200, null=True, blank=True)

    Geschlecht = models.CharField(
            max_length=1,
            choices=CharSex.choices,
            default=CharSex.FEMALE,
        )

    class Char_Class(models.TextChoices):
        W = 'W', gettext_lazy('Krieger')  # warrior: hp 200, ap 10
        P = 'P', gettext_lazy('Priester') # priest:  hp 75,  ap 5
        M = 'M', gettext_lazy('Zauberer') # mage:    hp 100, ap 20

    Klasse = models.CharField(
            max_length=1,
            choices=Char_Class.choices,
            default=Char_Class.W,
        )
    
    hp = models.IntegerField(default=0) 
    ap = models.IntegerField(default=0) 


    def __str__(self): # (TODO!) this maybe the cause of many problems... why do we need this? would it be better w/o? to fetch id's...
        return self.name


class GameScenes(models.Model): # blueprint of the games
    name = models.CharField(unique=True, max_length=300)
    req_players = models.BigIntegerField(default=1) # anzahl notweniger spieler
    welcome_text = models.TextField(default="Eine Gefahr zeigt sich im dunkeln...<br />Es raschelt...<br />", null=True, blank=True)
    enemy_name = models.CharField(default="Der Gegener", null=True, blank=True, max_length=300)
    enemy_hp = models.IntegerField(default=100) 
    enemy_ap =  models.IntegerField(default=10)
    enemy_image = models.CharField(default="hypnotoad.mp4", null=True, blank=True, max_length=300)
    
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

class Games(models.Model): # Here we find all information on games that were started, are being played and finished games. 
    created = models.DateTimeField(default=datetime.now) 
    game_scene_id = models.ForeignKey(GameScenes, on_delete=models.CASCADE)
    game_finished = models.BooleanField(default=False)
    locked_in_datetime = models.DateTimeField(null=True, blank=True)
    chat_log = models.TextField(default='', null=True, blank=True)
    game_log = models.TextField(default='', null=True, blank=True)
    enemy_current_hp = models.IntegerField(default=None, null=True, blank=True)
    round_state = models.IntegerField(default=0, null=True, blank=True)
    round_state_locked = models.BooleanField(default=False, null=True, blank=True)
    round_counter = models.IntegerField(default=0, null=True, blank=True)
    
class UserCharInGames(models.Model):
    game_id = models.ForeignKey(Games, on_delete=models.CASCADE)
    user_char_id = models.ForeignKey(UserChar, on_delete=models.CASCADE)
    current_hp = models.IntegerField(default=None, null=True, blank=True)
    current_ap = models.IntegerField(default=None, null=True, blank=True)
    user_char_died = models.BooleanField(default=False)
    next_action = models.TextField(default='', null=True, blank=True)
    next_action_was_reminded = models.BooleanField(default=False)
