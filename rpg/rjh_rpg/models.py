from django.db import models

# Create your models here.

class User(models.Model):
    nickname = models.CharField(unique=True,max_length=100)
    email = models.EmailField(unique=True)
    text = models.CharField(max_length=255, null=True, blank=True)