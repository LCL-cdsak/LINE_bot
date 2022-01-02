import os
import sys
import pygraphviz
from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,URIAction
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

machine = TocMachine(
    states=["init","fsm_graph","choose_information","choose_city","weather","choose_news_numbers","news","sport","global","breaknews","society"
    ,"show_1_news","show_3_news","show_5_news","return"],
    transitions=[
        {
            "trigger": "advance",
            "source": "init",
            "dest": "fsm_graph",
            "conditions": "is_going_to_fsm_graph",
        },
        {
            "trigger": "advance",
            "source": "init",
            "dest": "choose_information",
            "conditions": "is_going_to_choose_information",
        },
        {
            "trigger": "advance",
            "source": "choose_information",
            "dest": "news",
            "conditions": "is_going_to_news",
        },
        {
            "trigger": "advance",
            "source": "choose_information",
            "dest": "choose_city",  
            "conditions": "is_going_to_choose_city",
        },
        {
            "trigger": "advance",
            "source": "choose_city",
            "dest": "weather",  
            "conditions": "is_going_to_weather",
        },
        {
            "trigger": "advance",
            "source": "weather",
            "dest": "choose_city",
            "conditions": "is_going_to_back_choose_city",
        },
        {
            "trigger": "advance",
            "source": "choose_information",
            "dest": "choose_news_numbers",
            "conditions": "is_going_to_choose_news_numbers",
        },
        {
            "trigger": "advance",
            "source": "choose_news_numbers",
            "dest": "show_1_news",
            "conditions": "is_going_to_show_1_news",
        },
        {
            "trigger": "advance",
            "source": "choose_news_numbers",
            "dest": "show_3_news",
            "conditions": "is_going_to_show_3_news",
        },
        {
            "trigger": "advance",
            "source": "choose_news_numbers",
            "dest": "show_5_news",
            "conditions": "is_going_to_show_5_news",
        },
        {
            "trigger": "advance",
            "source": "news",
            "dest": "sport",
            "conditions": "is_going_to_sport",
        },
        {
            "trigger": "advance",
            "source": "news",
            "dest": "global",
            "conditions": "is_going_to_global",
        },
        {
            "trigger": "advance",
            "source": "news",
            "dest": "breaknews",
            "conditions": "is_going_to_breaknews",
        },
        {
            "trigger": "advance",
            "source": "news",
            "dest": "society",
            "conditions": "is_going_to_society",
        },
        {
            "trigger": "advance",
            "source": ["fsm_graph","choose_information","weather","sport","global","breaknews","society","show_1_news","show_3_news","show_5_news"],
            "dest": "init",
            "conditions": "is_going_to_init",
        },
        {
            "trigger": "advance",
            "source": ["fsm_graph","weather","sport","global","breaknews","society","choose_news_numbers","show_1_news","show_3_news","show_5_news"],
            "dest": "choose_information",
            "conditions": "is_going_to_back_choose_information",
        },
        {
            "trigger": "advance",
            "source": ["fsm_graph","choose_information","choose_city","weather","choose_news_numbers","news","sport","global","breaknews","society"
    ,"show_1_news","show_3_news","show_5_news","return"],
            "dest": "init",
            "conditions": "is_going_to_return",
        },
    ],
    initial="init",
    auto_transitions=False,
    show_conditions=True,
)
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
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if machine.state=="init":
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
            elif machine.state=="choose_city":
                send_text_message(event.reply_token,"請輸入正確的城市名稱，或輸入\"menu\"返回主選單")
            elif machine.state!="sport" and machine.state!="breaknews" and machine.state!="global" and machine.state!="society":
                send_text_message(event.reply_token,"請依照功能選單點選，或輸入\"menu\"返回主選單")
    return "OK"
    
@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
