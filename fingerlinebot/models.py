from django.db import models
from datetime import date

# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=200)
    mail = models.CharField(max_length=50)
    line_id = models.CharField(max_length=50)

class Ministry_Interior(models.Model):
    line_id = models.CharField(max_length=50)
    inform_date = models.DateField(default=date.today)

class Mails(models.Model):
    mail = models.CharField(max_length=50)
    used = models.CharField(max_length=5)