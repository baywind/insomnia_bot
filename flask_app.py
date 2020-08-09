# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from secrets import TARGET_CHAT_ID
from datetime import datetime, timedelta, timezone
import json

app = Flask(__name__)
tz = timezone(timedelta(hours=3))

history = []
history_size = 50


def log(js, to):
    row = [datetime.now(tz), js['message']['from'], to]
    history.append(row)
    while len(history) > history_size:
        del history[0]


def format_user(user):
    if 'username' in user:
        return user['username']
    else:
        if 'first_name' in user:
            return user['first_name']
        if 'last_name' in user:
                return user['last_name']


def print_log(n):
    n += 1
    result = []
    for row in history[-1:-n:-1]:
        s = [row[0].strftime('%d.%m %H:%M:%S'), format_user(row[1])]
        if isinstance(row[2], str):
            s.append(row[2])
        else:
            s.append('->')
            s.append(format_user(row[2]))
        result.append(' '.join(s))
    return '\n'.join(result)


@app.route('/')
def hello_world():
    return 'Test site is working!'


@app.route('/bot', methods=['POST'])
def get_update():
    js = request.json
    with open('requests.log', 'ta', encoding='utf8') as file:
        print('\n\n', datetime.now(tz), file=file, sep='')
        json.dump(js, file, ensure_ascii=False, indent=4)

    if 'message' in js:
        chat_id = js['message']['chat']['id']
        if js['message']['text'].startswith('/'):  # обработка команды
            text = js['message']['text']
            result = {
                'method': 'sendMessage',
                'chat_id': chat_id,
                "ok": True
            }
            log(js, text)
            if chat_id == TARGET_CHAT_ID:  # для своих
                if text.startswith('/log'):
                    n = 5
                    if len(text) > 5:
                        try:
                            n = int(text[5:])
                        except ValueError:
                            result['text'] = 'Принимается только целое число строк не более ' + \
                                str(history_size)
                            return result
                    result['text'] = print_log(n)
                else:
                    result['text'] = "Пока поддерживается только команда /log [n]\n" \
                                     "где n — количество последних записей. По умолчанию 5"
            else:  # для всех остальных
                if text.startswith('/start'):
                    result['text'] = '''Привет! Я простой и скромный бот-секретарь:
Перешлю твои сообщения в чатик Штаба строяка, а когда они ответят, перешлю тебе обратно ответ.'''
                else:
                    result['text'] = '''Не пытайся давать мне команды, я всё равно не пойму =(
Я умею только пересылать сообщения туда-обратно'''
            return result

        result = {
            'method': 'forwardMessage',
            'chat_id': TARGET_CHAT_ID,
            'from_chat_id': chat_id,
            'message_id': js['message']['message_id'],
            "ok": True
        }
        if chat_id == TARGET_CHAT_ID:
            try:
                result['chat_id'] = js['message']['reply_to_message']['forward_from']['id']
                log(js, js['message']['reply_to_message']['forward_from'])
            except KeyError:
                result['method'] = 'sendMessage'
                result['text'] = 'Так не работает. Можно только отвечать на пересланные сообщения.'
                result['reply_to_message_id'] = js['message']['message_id']
                log(js, '"Так не работает"')
        else:
            log(js, '-> Штаб Строяка')
        # print(js['message'])

        return result
    else:
        return {"ok": True}


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
