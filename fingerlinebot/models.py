from django.db import models

# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=200)
    mail = models.CharField(max_length=50)
    line_id = models.CharField(max_length=50)

class Ministry_Interior(models.Model):
    name = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=200)
    line_id = models.CharField(max_length=50)

class Mails(models.Model):
    mail = models.CharField(max_length=50)
    used = models.CharField(max_length=5)