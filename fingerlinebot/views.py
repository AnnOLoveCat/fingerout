from django.shortcuts import render

# Create your views here.'
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core import serializers
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import ( 
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction,
    PostbackAction,
)

from .models import Mails,News


import re
import urllib.parse
import requests
import json
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 


@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件

                #使用者的訊息
                user_msg = event.message.text.lower()
                
                #篩選資料庫裡的Mails資料
                accounts = Mails.objects.filter(mail=user_msg)
                # #篩選資料庫資料庫裡的News資料
                news_data = serializers.serialize('json', News.objects.all().filter(pk=1),fields=('news_title','news_content'))
                #回覆給使用者訊息
                message = []

                if user_msg == '更多功能':
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='更多功能',
                                text='請問要什麼功能?',
                                actions=[
                                    PostbackAction(
                                        label='新聞情報',
                                        text='新聞',
                                        data='新聞'
                                    ),
                                ]
                            )
                        )
                    )
                
                if user_msg == '新聞':
                    message.append(TextSendMessage(text=news_data))

                
                for account in accounts:
                    #判斷使用者輸入的帳號是否被使用過，回復傳入的訊息文字
                    if user_msg == account.mail and account.used == '是':
                        message.append(TextSendMessage(text= account.mail + '\n' +'此帳號有被使用過！！！'))
                    else:
                        message.append(TextSendMessage(text=account.mail + '\n' +'此帳號無被使用過，請放心～'))
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    message,
                )
                print(message)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def main(*args, **kwargs):
    return HttpResponse("<h1>Hello World!</h1>")