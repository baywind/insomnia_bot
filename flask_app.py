# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request

from BotInstance import BotInstance
from datetime import datetime
import json
import sqlalchemy
from model import SqlAlchemyBase
from texts import REGISTERED, UNKNOWN_BOT, ERROR_CREATING

app = Flask(__name__)
engine = sqlalchemy.create_engine('sqlite:///db.sqlite?check_same_thread=False', echo=False)
make_session = sqlalchemy.orm.sessionmaker(bind=engine)
SqlAlchemyBase.metadata.create_all(engine)


@app.route('/')
def hello_world():
    return 'Forwarder bot service is running!'


@app.route('/<bot_name>', methods=['POST'])
def get_update(bot_name):
    js = request.json
    # with open('requests.log', 'ta', encoding='utf8') as file:
    #     print('\n\n', datetime.now(), bot_name, file=file, sep='')
    #     json.dump(js, file, ensure_ascii=False, indent=4)

    if 'message' in js:
        ses: sqlalchemy.orm.Session = make_session()
        bot: BotInstance = ses.query(BotInstance).filter(BotInstance.name == bot_name).first()

        msg = js['message']
        chat_id = msg['chat']['id']
        if not bot:
            result = {
                'method': 'sendMessage',
                'chat_id': chat_id,
                'ok': True
            }
            if chat_id > 0 and 'text' in msg and msg['text'] == '/register':
                try:
                    bot = BotInstance()
                    bot.name = bot_name
                    bot.owner_id = chat_id
                    ses.add(bot)
                    ses.commit()
                    result['text'] = REGISTERED % bot_name
                except Exception as e:
                    result['text'] = ERROR_CREATING + e
            else:
                result['text'] = UNKNOWN_BOT
            return result

        if 'text' in msg and msg['text'].startswith('/'):  # обработка команды
            quote = None
            if 'reply_to_message' in msg:
                quote = msg['reply_to_message']
            entities = []
            text = bot.command(msg['chat']['id'],
                               msg['text'],
                               msg['from'],
                               quote, entities)
            result = {
                'method': 'sendMessage',
                'chat_id': js['message']['chat']['id'],
                'text': text,
                'ok': True,
                'entities': entities
            }
        else:
            result = bot.forward_message(js)
        ses.commit()
        return result
    else:
        return {"ok": True}


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
