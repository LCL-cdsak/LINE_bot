from transitions.extensions import GraphMachine
from linebot import LineBotApi
from utils import send_text_message,send_button_message,send_CarouselColumn_message,send_multiple_text_message
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    CarouselTemplate, 
    CarouselColumn,
    URIAction,
    MessageAction
)
from linebot import LineBotApi
import requests
from bs4 import BeautifulSoup
import json
import os
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.news_num = 1
        self.city = ""
    def udn_crawling(self,event,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        image = soup.find_all(
            'div',{'class': 'story-list__image'} ,limit=5)
        content = soup.find_all(
            'div',{'class': 'story-list__text'} ,limit=5)
        images = []
        for img in image:
            images.append(img.a.picture.source.get("data-srcset"))
        titles = []
        for img in image:
            titles.append(img.a.get("aria-label"))
        urls = []
        for img in image:
            urls.append("https://udn.com/"+img.a.get("href"))
        contents = []
        for t in content:
            contents.append(t.p.text.lstrip())
        column = []
        for i in range(len(image)):
            c = CarouselColumn(
                            thumbnail_image_url= images[i],
                            title=titles[i],
                            text=" ",
                            actions=[
                                MessageAction(
                                 label='查看大綱',
                                 text = contents[i]
                             ),
                                URIAction(
                                    label='查看新聞',
                                    uri=urls[i]
                                )
                            ]
                        )
            column.append(c)
        column.append(CarouselColumn(
                            thumbnail_image_url= "https://imgur.com/Daaf6o9.png",
                            title="請選擇想使用的功能",
                            text=" ",
                            actions=[
                                MessageAction(
                                 label="返回功能選單",
                                 text = "返回功能選單"
                             ),
                             MessageAction(
                                 label="返回資訊選單",
                                 text = "返回資訊選單"
                             ),
                            ]
                        ))
        send_CarouselColumn_message(event.reply_token,column)
    def weather_api(self):
        token = 'CWB-08D3FE02-FCFD-4E41-A371-3BB252782EBD'
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + self.city
        Data = requests.get(url)
        Data = (json.loads(Data.text))['records']['location'][0]['weatherElement']
        res = [[] , [] , []]
        for j in range(3):
            for i in Data:
                res[j].append(i['time'][j])
        return res

    def is_going_to_init(self,event):
        return event.message.text == "返回功能選單"
    def is_going_to_choose_information(self,event): 
        return event.message.text == "開始使用"
    def is_going_to_fsm_graph(self,event):
        return event.message.text == "fsm_graph"
    def is_going_to_github(self,event):
        return event.message.text == "github"
    def is_going_to_choose_news_numbers(self,event):
        return event.message.text == "成大即時新聞"
    def is_going_to_news(self, event):
        return event.message.text == "新聞"
    def is_going_to_choose_city(self,event):
        return event.message.text == "天氣"
    def is_going_to_weather(self,event):
        event.message.text = event.message.text.replace('台','臺')
        city = ['基隆市','嘉義市','臺北市','嘉義縣','新北市','臺南市','桃園縣','高雄市','新竹市','屏東縣','新竹縣','臺東縣','苗栗縣','花蓮縣','臺中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']
        for item in city:
            if(event.message.text == item):
                self.city = item
                return True
        return False
    def is_going_to_show_1_news(self,event):
        return event.message.text == "1"
    def is_going_to_show_3_news(self,event):
        return event.message.text == "3"
    def is_going_to_show_5_news(self,event):
        return event.message.text == "5"
    def is_going_to_sport(self, event):
        return event.message.text == "運動"
    def is_going_to_global(self, event):
        return event.message.text == "全球"
    def is_going_to_breaknews(self, event):
        return event.message.text == "即時"
    def is_going_to_society(self, event):
        return event.message.text == "社會"
    def is_going_to_back_choose_information(self,event):
        return event.message.text == "返回資訊選單"
    def is_going_to_back_choose_city(self,event):
        return event.message.text == "查詢其他縣市天氣"
    def is_going_to_return(self,event):
        return (event.message.text == "menu" or event.message.text == "Menu")
    def on_enter_init(self,event):
        title="選擇你想使用的功能"
        text=" "
        btn = [
            MessageTemplateAction(
                label = '開始使用',
                text ='開始使用'
            ),
            MessageTemplateAction(
                label = 'fsm graph',
                text ='fsm graph'
            ),
            MessageTemplateAction(
                label = 'github',
                text = 'github'
            ),
        ]
        send_button_message(event.reply_token, title, text, btn,"https://imgur.com/YFQlysd.png")
    def on_enter_choose_news_numbers(self,event):
        title="選擇你想查閱的新聞數量"
        text=" "
        btn = [
            MessageTemplateAction(
                label = '1',
                text ='1'
            ),
            MessageTemplateAction(
                label = '3',
                text ='3'
            ),
            MessageTemplateAction(
                label = '5',
                text = '5'
            ),
            MessageTemplateAction(
                label = '返回資訊選單',
                text = '返回資訊選單'
            ),
        ]
        send_button_message(event.reply_token, title, text, btn,"https://imgur.com/ZB6yVsJ.png")
    def on_enter_choose_information(self,event):
        title="選擇你想查詢的資訊"
        text="成大新聞、udn新聞、天氣"
        btn = [
            MessageTemplateAction(
                label = '天氣',
                text = '天氣'
            ),
            MessageTemplateAction(
                label = 'udn新聞',
                text = '新聞'
            ),
            MessageTemplateAction(
                label = '成大即時新聞',
                text = '成大即時新聞'
            ),
            MessageTemplateAction(
                label = '返回功能選單',
                text = '返回功能選單'
            ),
        ]
        send_button_message(event.reply_token, title, text, btn,"https://imgur.com/0ByPrqI.png")
    def on_enter_news(self,event):
        title="選擇你想查詢的新聞"
        text="運動、全球、即時、社會"
        btn = [
            MessageTemplateAction(
                label = '運動',
                text ='運動'
            ),
            MessageTemplateAction(
                label = '全球',
                text ='全球'
            ),
            MessageTemplateAction(
                label = '即時',
                text = '即時'
            ),
            MessageTemplateAction( 
                label = '社會',
                text = '社會'
            ),
        ]
        send_button_message(event.reply_token, title, text, btn,"https://imgur.com/rFB2nY7.png")
    def on_enter_show_1_news(self,event):
        response = requests.get('https://news-secr.ncku.edu.tw/p/412-1037-5934.php')
        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all(
                    'div', {'class': 'row listBS boxSD'}, limit=1)
        urls = []
        for t in cards:
            urls.append(t.div.div.div.div.a.get("href"))
        send_multiple_text_message(event.reply_token,urls)
    def on_enter_show_3_news(self,event):
        response = requests.get('https://news-secr.ncku.edu.tw/p/412-1037-5934.php')
        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all(
                    'div', {'class': 'row listBS boxSD'}, limit=3)
        urls = []
        for t in cards:
            urls.append(t.div.div.div.div.a.get("href"))
        send_multiple_text_message(event.reply_token,urls)
    def on_enter_show_5_news(self,event):
        response = requests.get('https://news-secr.ncku.edu.tw/p/412-1037-5934.php')
        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all(
                    'div', {'class': 'row listBS boxSD'}, limit=5)
        urls = []
        for t in cards:
            urls.append(t.div.div.div.div.a.get("href"))
        send_multiple_text_message(event.reply_token,urls)
    def on_enter_breaknews(self,event):
        url = 'https://udn.com/news/cate/2/6638'
        self.udn_crawling(event,url)
    def on_enter_sport(self,event):
        url = 'https://udn.com/news/cate/2/7227'
        self.udn_crawling(event,url)
    def on_enter_global(self,event):
        url = 'https://udn.com/news/cate/2/7225'
        self.udn_crawling(event,url)
    def on_enter_society(self,event):
        url = 'https://udn.com/news/cate/2/6639'
        self.udn_crawling(event,url)
    def on_enter_choose_city(self,event):
        send_text_message(event.reply_token,"請輸入想查詢的城市")
    def on_enter_weather(self,event):
        res = self.weather_api()
        line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None))
        result = []
        result.append(TemplateSendMessage(
            alt_text = self.city + '未來 36 小時天氣預測',
            template = CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url = 'https://imgur.com/1Aj7zmx.png',
                        title = '{} ~ {}'.format(data[0]['startTime'][5:-3],data[0]['endTime'][5:-3]),
                        text = '天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}'.format(data[0]['parameter']['parameterName'],data[2]['parameter']['parameterName'],data[4]['parameter']['parameterName'],data[1]['parameter']['parameterName']),
                        actions = [
                            URIAction(
                                label = '詳細資料',
                                uri = 'https://www.cwb.gov.tw/V8/C/W/County/index.html'
                            )
                        ]
                    )for data in res
                ]
            )
        ))
        result.append(
        TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = "請選擇想使用的功能",
            text = " ",
            actions = [
            MessageTemplateAction(
                label ='查詢其他縣市天氣',
                text ='查詢其他縣市天氣'
            ),
            MessageTemplateAction(
                label = '返回功能選單',
                text ='返回功能選單'
            ),
            MessageTemplateAction(
                label = '返回資訊選單',
                text ='返回資訊選單'
            ),],
            thumbnail_image_url= "https://imgur.com/Daaf6o9.png"
        )
        )
        )
        line_bot_api.reply_message(event.reply_token, result)