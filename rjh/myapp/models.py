from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Webpage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.RESTRICT)
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField(unique=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class AccessRecord(models.Model):
    name = models.ForeignKey(Webpage, on_delete=models.RESTRICT)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.date)


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)