# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request

from BotInstance import BotInstance
from datetime import datetime, timedelta, timezone
import json

app = Flask(__name__)
bot = BotInstance()


@app.route('/')
def hello_world():
    return 'Test site is working!'


@app.route('/bot', methods=['POST'])
def get_update():
    js = request.json
    with open('requests.log', 'ta', encoding='utf8') as file:
        print('\n\n', datetime.now(), file=file, sep='')
        json.dump(js, file, ensure_ascii=False, indent=4)

    if 'message' in js:
        # chat_id = js['message']['chat']['id']
        if js['message']['text'].startswith('/'):  # обработка команды
            return bot.command(js['message']['chat']['id'], js['message']['text'])
        else:
            return bot.forward_message(js)
    else:
        return {"ok": True}


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
