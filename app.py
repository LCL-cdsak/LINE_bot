import os
import sys
import pygraphviz
from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,URIAction
from machine import create_machine
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

from fsm import TocMachine
from utils import send_text_message,send_button_message

load_dotenv()

machines = {}
m = create_machine()
#machine.get_graph().draw("./img/fsm.jpg", prog="dot", format="jpg")

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        if event.source.user_id not in machines:
            machines[event.source.user_id] = create_machine()
        response = machines[event.source.user_id].advance(event)
        if response == False:
            if machines[event.source.user_id].state=="init":
                #send_text_message(event.reply_token,"rechoose city")
                title="\t\t選擇你想使用的功能"
                text=" "
                btn = [
                    MessageTemplateAction(
                        label = '開始使用',
                        text ='開始使用'
                    ),
                    MessageTemplateAction(
                        label = 'fsm_graph',
                        text ='fsm_graph'
                    ),
                    URIAction(
                                label = 'github',
                                uri = 'https://github.com/LCL-cdsak/LINE_bot'
                            )
                ]
                send_button_message(event.reply_token, title, text, btn,"https://imgur.com/YFQlysd.png")
            elif machines[event.source.user_id].state=="choose_city":
                send_text_message(event.reply_token,"請輸入正確的城市名稱，或輸入\"menu\"返回主選單")
            elif machines[event.source.user_id].state!="sport" and machines[event.source.user_id].state!="breaknews" and machines[event.source.user_id].state!="global" and machines[event.source.user_id].state!="society":
                send_text_message(event.reply_token,"請依照功能選單點選，或輸入\"menu\"返回主選單")
    return "OK"
    
@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    m.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
