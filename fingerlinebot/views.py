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

from .models import *


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

#額外的News資料，顯示全部的News
news_all_information = News.objects.all().values_list('news_content',flat=True)
news_all_data = json.dumps(list(news_all_information),ensure_ascii=False)
news_all_result = json.loads(news_all_data)
# news_all_title = News.objects.all().values_list('news_title',flat=True)
# news_all_content = News.objects.all().values_list('news_content',flat=True)

# news_title_data = json.dumps(list(news_all_title),ensure_ascii=False)
# news_content_data = json.dumps(list(news_all_content),ensure_ascii=False)

# news_title_result = json.loads(news_title_data)
# news_content_result = json.loads(news_content_data)

#篩選資料庫資料庫裡的Ministry_Interior資料
lineid_information = Ministry_Interior.objects.all().values_list('line_id',flat=True)
lineid_data = json.dumps(list(lineid_information),ensure_ascii=False)
lineid_result = json.loads(lineid_data)

#篩選資料庫資料庫裡的Links資料
links_information = Links.objects.all().values_list('web_link',flat=True)
links_data = json.dumps(list(links_information),ensure_ascii=False)
links_result = json.loads(links_data)

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
                #Line ID的資料
                lineid = Ministry_Interior.objects.filter(line_id=user_msg)
                #Links的資料
                fake_link = Links.objects.filter(web_link=user_msg)
                #比照資料庫裡的Mails資料
                accounts = Mails.objects.filter(mail=user_msg)
                #回覆給使用者訊息
                message = []
                message.clear()

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
                                            label='最新新聞',
                                            text='最新新聞',
                                            data='最新新聞'
                                        ),
                                    ]
                                ),
                                CarouselColumn(
                                    title='詐騙新聞情報',
                                    text='顯示目前最新新聞',
                                    actions=[
                                        PostbackAction(
                                            label='所有新聞',
                                            text='所有新聞',
                                            data='所有新聞'
                                        ),
                                    ]
                                ),
                                CarouselColumn(
                                    title='詐騙用戶',
                                    text='顯示目前最近所有的詐騙用戶',
                                    actions=[
                                        PostbackAction(
                                            label='詐騙用戶',
                                            text='詐騙用戶',
                                            data='詐騙用戶'
                                        ),
                                    ]
                                ),
                                CarouselColumn(
                                    title='詐騙網址',
                                    text='顯示目前最近所有的詐騙網址',
                                    actions=[
                                        PostbackAction(
                                            label='詐騙網址',
                                            text='詐騙網址',
                                            data='詐騙網址'
                                        ),
                                    ]
                                ),
                                CarouselColumn(
                                    title='查詢網址',
                                    text='輸入網址，幫您查詢目前網址是否為詐騙網址',
                                    actions=[
                                        PostbackAction(
                                            label='查詢網址',
                                            text='查詢網址',
                                            data='查詢網址'
                                        ),
                                    ]
                                ),
                                CarouselColumn(
                                    title='查詢帳號',
                                    text='查詢目前帳號是否存在並幫您查詢有被外洩的問題',
                                    actions=[
                                        PostbackAction(
                                            label='查詢帳號',
                                            text='查詢帳號',
                                            data='查詢帳號'
                                        ),
                                    ]
                                ),
                                CarouselColumn(
                                    title='新增帳號',
                                    text='新增帳號，以助於之後能夠查詢是否有被外洩的問題',
                                    actions=[
                                        PostbackAction(
                                            label='新增帳號',
                                            text='新增帳號',
                                            data='新增帳號'
                                        ),
                                    ]
                                )
                            ]
                        )
                    )
            )
                    
                if user_msg == '最新新聞':
                    title = news_result[0]['news_title']
                    content = news_result[0]['news_content']
                    message.append(TextSendMessage(text = '最新新聞：'+ "\n" + title + "\n" + '內容：' + content))
                
                if user_msg == '詐騙用戶':
                    message.append(TextSendMessage(text = '最近的詐騙ID: '+ "\n" + lineid_data.replace(',', "\n").replace('[', '').replace(']', '').replace('"', '')))

                
                if user_msg == '查詢網址':
                    message.append(TextSendMessage(text = '請輸入網址'))
                    
                if user_msg == '詐騙網址':
                    all_links = [item.replace(',','\n') for item in links_result]
                    
                    for num,part_links in enumerate(all_links):
                        if num == 5:
                            break
                        message.append(TextSendMessage(text = '最近的詐騙網址： '+ "\n" + part_links))

                if user_msg == '所有新聞':
                    all_news = [item.replace(',','\n') for item in news_all_result]
                    
                    for num,part_news in enumerate(all_news):
                        if num == 5:
                            break
                        message.append(TextSendMessage(text = '第'+ str(num+1) + '則' + "\n" + part_news))

                if user_msg == '查詢帳號' or user_msg == '新增帳號':
                    message.append(TextSendMessage(text = '請輸入帳號'))

                if accounts.exists() and '@'in user_msg:
                    message.append(TextSendMessage(text = '有此帳號歐'))
                elif '@' not in user_msg:
                    pass
                else:
                    message.append(TextSendMessage(text = '無此帳號歐 ' + '\n' + '正在幫您把目前輸入的帳號新增置資料庫'))
                    
                    Mails.objects.create(mail=user_msg)

                    if accounts.exists():
                        message.append(TextSendMessage(text = '已幫您新增至資料庫，請等待人員幫您檢測帳號是否有被外洩'))
                    else:
                        message.append(TextSendMessage(text = '無法新增至資料庫，請等待人員幫您檢測'))
                        
                
                #詐騙Line ID
                for line in lineid:
                    if user_msg == line.line_id:
                        message.append(TextSendMessage(text= '有此詐騙ID: ' + user_msg))
                    else:
                        message.append(TextSendMessage(text= '無此詐騙ID: ' + user_msg))


                #詐騙網址
                for link in fake_link:
                    if user_msg == link.web_link:
                        message.append(TextSendMessage(text= '有此詐騙網址: ' + user_msg))
                    else:
                        message.append(TextSendMessage(text= '無此詐騙網址: ' + user_msg))


                for account in accounts:
                    #判斷使用者輸入的帳號是否被使用過，回復傳入的訊息文字
                    if user_msg == account.mail and account.used == '是':
                        message.append(TextSendMessage(text = account.mail + "\n" +'此帳號有外洩風險！！！'))
                    elif user_msg == account.mail and len(account.used) == 0: 
                        message.append(TextSendMessage(text = account.mail + "\n" +'目前人員還在幫您檢測，會盡快幫您確認請放心～'))
                    else:
                        message.append(TextSendMessage(text = account.mail + "\n" +'此帳號無風險，請放心～'))

                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    message,
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def main(*args, **kwargs):
    return HttpResponse("<h1>Hello World!</h1>")