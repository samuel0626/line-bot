from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('0Wv8a1j4MnpsK542KmC5B0w6kgLkXNBsZ0hc2bAdY5bjbg0qhEk8i88CcjXizxRs89mUMsZ7bMOnhkY4XQFn5x2g3yfl34OpyaF4afGP4rohV4+CiVSvXsBXCM95cMMPJrYmYMEhyVbkzaVfTEeUOgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0ce703d864296771c84dff3ba1a06d15')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()