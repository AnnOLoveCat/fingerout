from django.contrib import admin
from fingerlinebot.models import *

# Register your models here.
class Message_Admin(admin.ModelAdmin):
    list_display = ('name','time','url','mail','line_id')
admin.site.register(Message,Message_Admin)

class Ministry_Interior_Admin(admin.ModelAdmin):
    list_display = ('line_id','inform_date')
admin.site.register(Ministry_Interior,Ministry_Interior_Admin)

class Mails_Admin(admin.ModelAdmin):
    list_display = ('mail','used')
admin.site.register(Mails,Mails_Admin)

class News_Admin(admin.ModelAdmin):
    list_display = ('news_title','post_time','news_content')
admin.site.register(News,News_Admin)

class Links_Admin(admin.ModelAdmin):
    list_display = ('description','web_link','domain_name','build_time')
admin.site.register(Links,Links_Admin)


