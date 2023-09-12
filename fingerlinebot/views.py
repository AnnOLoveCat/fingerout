from django.shortcuts import render

# Create your views here.'
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core import serializers
from django.forms import model_to_dict
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import ( 
    MessageEvent,
    TextSendMessage,
    LocationMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction,
    PostbackAction,
    MessageAction,
    CarouselTemplate,
    CarouselColumn
)

from .models import Mails,News,Ministry_Interior


import re
import urllib.parse
import requests
import json
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 

#篩選資料庫資料庫裡的News資料
news_information = News.objects.all().values('news_title','news_content').filter(pk=1)
news_data = json.dumps(list(news_information),ensure_ascii=False)
news_result = json.loads(news_data)
#篩選資料庫資料庫裡的Ministry_Interior資料
lineid_information = Ministry_Interior.objects.all().values('line_id')
lineid_data = json.dumps(list(lineid_information),ensure_ascii=False)
lineid_result = json.loads(lineid_data)

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
                #回覆給使用者訊息
                message = []

                #功能選單
                if user_msg == '更多功能':
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                        alt_text='Carousel template',
                        template=CarouselTemplate(
                            columns=[
                                CarouselColumn(
                                    title='詐騙新聞情報',
                                    text='顯示目前最新新聞',
                                    actions=[
                                        PostbackAction(
                                            label='新聞情報',
                                            text='新聞',
                                            data='新聞'
                                        ),
                                    ]
                                ),
                                CarouselColumn(
                                    title='詐騙Line ID',
                                    text='顯示目前最近所有的Line ID',
                                    actions=[
                                        PostbackAction(
                                            label='詐騙Line ID',
                                            text='詐騙',
                                            data='詐騙'
                                        ),
                                    ]
                                )
                            ]
                        )
                    )
            )
                    
                if user_msg == '新聞':
                    title = news_result[0]['news_title']
                    content = news_result[0]['news_content']
                    message.append(TextSendMessage(text = '最新新聞：'+ '\n' + title + '\n' + '內容：' + content))

                if user_msg == '詐騙':
                    message.clear()
                    message.append(TextSendMessage(text = '最近的詐騙ID: '+ '\n' + lineid_data))

                
                for account in accounts:
                    #判斷使用者輸入的帳號是否被使用過，回復傳入的訊息文字
                    if user_msg == account.mail and account.used == '是':
                        message.append(TextSendMessage(text = account.mail + '\n' +'此帳號有被使用過！！！'))
                    else:
                        message.append(TextSendMessage(text = account.mail + '\n' +'此帳號無被使用過，請放心～'))

                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    message,
                )
                print(lineid_data)
                print(type(lineid_data))
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def main(*args, **kwargs):
    return HttpResponse("<h1>Hello World!</h1>")