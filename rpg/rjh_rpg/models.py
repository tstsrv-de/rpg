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
    
    
class GameState(models.Model):
    
    char = models.ForeignKey(UserChar, on_delete=models.CASCADE, unique=True)
    place = models.IntegerField(default=0)
    charLogin = models.DateTimeField(default=datetime.now) 
    char_user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE, null=True, blank=True)