from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    PostbackEvent,
    QuickReply,
    PostbackAction,
    QuickReplyButton,
)
import os
from pykintone import model
import pykintone

# from kintone-main.question import Question

from answer import *
from answer_rate import *
from choice import *
from correct_answer import *
from get_question import *
from question import *
from setting import *

app = Flask(__name__)


@app.route("/test")
def test():
    return "<h1>It Works!</h1>"


# 環境変数取得
line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])

# question_id=0
# maxqunum=3
question_id = 0

## 1 ##
# Webhookからのリクエストをチェックします。
@app.route("/callback", methods=["POST"])
def callback():
    print("ok")
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers["X-Line-Signature"]
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


## 2 ##
###############################################
# LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################
# LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
# def以下の関数を実行します。
# reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。
# 第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 正誤判定記述

    print(vars(event))

    global question_id

    result = event.message.text  # 回答
    print(question_id)
    correct = get_question_correct_answers(question_id)  # 解答

    profile = line_bot_api.get_profile(event.source.user_id)
    user_id = event.source.user_id  # ユーザID (zzz)

    print(user_id)

    post_answer(question_id, result, user_id)  # question_id, content, user_id

    ranklist = obtain_ranking(int(question_id))

    print(ranklist)
    for user_data in ranklist:
        list_user_id = user_data["user_id"]
        list_user_rank = user_data["num"]
        list_user_time = user_data["time"]
        print(str(user_id) + " " + str(list_user_id))
        if user_id == list_user_id:
            rank = list_user_rank
            endtext = str(rank) + "位！"
            break

    if result == correct:
        ansmes = "正解！" + str(endtext)
    else:
        ansmes = "残念、不正解"

    # ansmes=result
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ansmes))


# 選択肢
@app.route("/four/<qunum>")
def sendmessage(qunum):
    global question_id
    question_id = qunum

    qutext = get_question_text(question_id)

    qutype = get_question_type(question_id)

    if qutype == "0":  # 問題が4択だったら
        items = []
        items.append(QuickReplyButton(action=PostbackAction(label="1", data="1")))
        items.append(QuickReplyButton(action=PostbackAction(label="2", data="2")))
        items.append(QuickReplyButton(action=PostbackAction(label="3", data="3")))
        items.append(QuickReplyButton(action=PostbackAction(label="4", data="4")))

        messages = TextSendMessage(text=qutext, quick_reply=QuickReply(items=items))
        line_bot_api.broadcast(messages=messages)
    elif qutype == "1":  # 問題が記述だったら
        messages = TextSendMessage(text=qutext)
        line_bot_api.broadcast(messages=messages)

    return "<h1>It Works!</h1>"


@handler.add(PostbackEvent)
def handle_postmessage(event):
    print(vars(PostbackEvent))

    print(event.postback.data)
    correct = get_question_correct_answers(question_id)
    result = event.postback.data  # 回答
    profile = line_bot_api.get_profile(event.source.user_id)
    user_id = event.source.user_id  # ユーザID (zzz)
    post_answer(question_id, result, user_id)  # question_id, content, user_id

    if result == correct:
        ansmes = "正解！"
    else:
        ansmes = "残念、不正解"
    # ansmes=result
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ansmes))


@app.route("/four/end/<qunum>")
def question_end(qunum):
    qutype = get_question_type(qunum)
    if qutype == "1":  # 問題が記述だったら
        profile = line_bot_api.get_profile(event.source.user_id)
        user_id = event.source.user_id  # ユーザID (zzz)

        ranklist = obtain_ranking(question_id)
        for user_data in ranklist:
            list_user_id = user_data["user_id"]
            list_user_rank = user_data["num"]
            list_user_time = user_data["time"]
            if user_id == list_user_id:
                rank = list_user_rank
                break
        endtext = rank + "位！"
        line_bot_api.push_message(user_id, TextSendMessage(text=endtext))
    elif qutype == "0":  # 問題が４択だったら
        endtext = get_answer_rate(question_id)
        messages = TextSendMessage(text=endtext)
        line_bot_api.broadcast(messages=messages)

    questions = question_app.select().models(Question)
    print(vars(questions[0]))

    return "<h1>解答の割合</h1>"


# ポート番号の設定
if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
