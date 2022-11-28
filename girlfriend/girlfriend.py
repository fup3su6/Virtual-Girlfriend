#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, abort
import configparser
from linebot import (
    LineBotApi, WebhookHandler
)
from nlp.olami import Olami
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")
line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Olami().nli(event.message.text)))

if __name__ == "__main__":
    app.run()

