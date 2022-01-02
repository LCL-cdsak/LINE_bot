import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, URITemplateAction, ButtonsTemplate, MessageTemplateAction, ImageSendMessage
from linebot.models import PostbackAction, MessageAction, URIAction, CarouselColumn, CarouselTemplate, PostbackTemplateAction, FlexSendMessage
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"
def send_multiple_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    messages = []
    for item in text:
        messages.append(TextSendMessage(item))
    line_bot_api.reply_message(reply_token, messages)

    return "OK"
def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"
def send_button_message(reply_token,title, text, btn,url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            actions = btn,
            thumbnail_image_url= url
        ),
        
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"
def send_CarouselColumn_message(reply_token,column):
    line_bot_api = LineBotApi(channel_access_token)
    carousel_template_message = []
    carousel_template_message.append (TemplateSendMessage(
             alt_text='新聞',
             template=CarouselTemplate(
                columns=column
             )
         )
    )
    line_bot_api.reply_message(reply_token, carousel_template_message)
    return "OK"

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
