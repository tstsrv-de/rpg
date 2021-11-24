from django.db import models

# Create your models here.

class User(models.Model):
    nickname = models.CharField(unique=True,max_length=100)
    email = models.EmailField(unique=True)
    text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nickname
    
    
class UserChar(models.Model):
    usernickname = models.ForeignKey(User, on_delete=models.RESTRICT)
    name = models.CharField(unique=True,max_length=100)
    
    def __str__(self):
        return self.name
    
    