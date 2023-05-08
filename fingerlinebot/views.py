from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from .models import Mails

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
                msg = event.message.text

                #資料庫裡的Mails資料，帳號跟被使用的是否
                accounts = Mails.objects.filter(mail=msg)
                
                #回覆使用者訊息
                content = ''
                
                for account in accounts:

                    #判斷使用者輸入的帳號是否被使用過
                    if msg == account.mail and account.used == '是':
                        content += account.mail + '\n' +'此帳號有被使用過！！！'
                    else:
                        content += account.mail + '\n' +'此帳號無被使用過，請放心～'

                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=content),
                )
                print(content)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def main(*args, **kwargs):
    return HttpResponse("<h1>Hello World!</h1>")