# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from secrets import TARGET_CHAT_ID
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Test site is working!'


@app.route('/bot', methods=['POST'])
def get_update():
    with open('requests.log', 'ta', encoding='utf8') as file:
        print(datetime.today(), request.get_data(as_text=True), file=file, end='\n\n')
    js = request.json
    if 'message' in js:
        chat_id = js['message']['chat']['id']
        result = {
            'method': 'forwardMessage',
            'chat_id': TARGET_CHAT_ID,
            'from_chat_id': chat_id,
            'message_id': js['message']['message_id'],
            "ok": True
        }
        if chat_id == TARGET_CHAT_ID:
            result['chat_id'] = js['message']['reply_to_message']['forward_from']['id']
        # print(js['message'])
        return result
    else:
        return {"ok": True}


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
