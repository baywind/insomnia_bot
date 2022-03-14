from datetime import timezone, timedelta, datetime

history_size = 50


def format_user(user):
    if 'username' in user:
        return '@' + user['username']
    else:
        if 'first_name' in user:
            return user['first_name']
        if 'last_name' in user:
            return user['last_name']


class BotInstance:
    unknown_command = '''Не пытайся давать мне команды, я всё равно не пойму =(
Я умею только пересылать сообщения туда-обратно'''

    def __init__(self):
        self.target_chat_id = -1
        self.tz = timezone(timedelta(hours=3))
        self.history = []
        self.start_text = '''Привет! Я простой и скромный бот-секретарь:
    Перешлю твои сообщения в чатик Штаба строяка, а когда они ответят, перешлю тебе обратно ответ.'''

    def log(self, js, to):
        row = [datetime.now(self.tz), js['message']['from'], to]
        self.history.append(row)
        while len(self.history) > history_size:
            del self.history[0]

    def command(self, from_chat, text):
        result = {
            'method': 'sendMessage',
            'chat_id': from_chat,
            "ok": True
        }
        if from_chat == self.target_chat_id:  # для своих
            if text.startswith('/log'):
                result['text'] = self.get_log_command(text)
        else:  # для всех остальных
            if text.startswith('/start'):
                result['text'] = self.start_text
            else:
                result['text'] = self.unknown_command
        return result

    def get_log_command(self, text):
        n = 5
        if len(text) > 5:
            try:
                n = int(text[5:])
            except ValueError:
                return 'Принимается только целое число строк не более ' + \
                       str(history_size)
        return self.print_log(n)

    def print_log(self, n):
        n += 1
        result = []
        for row in self.history[-1:-n:-1]:
            s = [row[0].strftime('%d.%m %H:%M:%S'), format_user(row[1])]
            if isinstance(row[2], str):
                s.append(row[2])
            else:
                s.append('->')
                s.append(format_user(row[2]))
            result.append(' '.join(s))
        return '\n'.join(result)

    def forward_message(self, js):
        chat_id = js['message']['chat']['id']

        result = {
            'method': 'forwardMessage',
            'chat_id': self.target_chat_id,
            'from_chat_id': chat_id,
            'message_id': js['message']['message_id'],
            "ok": True
        }
        if chat_id == self.target_chat_id:
            try:
                result['chat_id'] = js['message']['reply_to_message']['forward_from']['id']
                self.log(js, js['message']['reply_to_message']['forward_from'])
            except KeyError:
                result['method'] = 'sendMessage'
                result['text'] = 'Так не работает. Можно только отвечать на пересланные сообщения.'
                result['reply_to_message_id'] = js['message']['message_id']
                self.log(js, '"Так не работает"')
        else:
            self.log(js, '-> Штаб Строяка')
        # print(js['message'])

        return result
