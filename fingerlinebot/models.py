from django.db import models
from datetime import date,datetime

format = '%Y/%m/%d'
# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=200)
    mail = models.CharField(max_length=50)
    line_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name,self.time,self.url,self.mail,self.line_id
    

class Ministry_Interior(models.Model):
    line_id = models.CharField(max_length=50)
    inform_date = models.DateField(auto_now='%Y/%m/%d')

    def __str__(self):
        return self.line_id,self.inform_date

class Mails(models.Model):
    mail = models.CharField(max_length=50)
    used = models.CharField(max_length=5)

    def __str__(self):
        return self.mail,self.used
    

class News(models.Model):
    news_title = models.CharField(max_length=50)
    post_time = models.DateTimeField(auto_now='%Y/%m/%d %H:%M')
    news_content = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.news_title,self.post_time,self.news_content

class Links(models.Model):
    description = models.CharField(max_length=50)
    web_link = models.CharField(max_length=500)
    domain_name = models.CharField(max_length=50)
    build_time = models.DateTimeField(auto_now='%Y/%m/%d %H:%M')

    def __str__(self):
        return self.description,self.web_link,self.domain_name,self.build_time
    
