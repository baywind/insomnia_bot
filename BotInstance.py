from datetime import timezone, timedelta, datetime
from model import BotModel, MessageLog
import texts


def format_user(user):
    if 'username' in user:
        return '@' + user['username']
    else:
        if 'first_name' in user:
            return user['first_name']
        if 'last_name' in user:
            return user['last_name']


class BotInstance(BotModel):

    def tz(self):
        return timezone(timedelta(hours=self.timezone))

    def command(self, from_chat, text, from_id):
        if text.startswith('/start'):
            return self.start_text

        elif text == '/attach' and from_id == self.owner_id:
            return self.attach_chat(from_chat)

        elif text.startswith('/log') and from_chat in (self.owner_id, self.target_chat_id):
            return self.get_log_command(text)

        elif from_chat == self.owner_id:  # Администрирование
            if text.startswith('/timezone'):
                return self.set_timezone(text[10:])
            elif text.startswith('/greeting'):
                return self.set_greeting(text[10:])
            else:
                return texts.ADM_HELP

        elif from_chat == self.target_chat_id:
            return texts.CHAT_HELP

        else:
            return texts.UNKNOWN_COMMAND

    def get_log_command(self, text):
        n = 5
        if len(text) > 5:
            try:
                n = int(text[5:])
            except ValueError as e:
                return str(e)

        log = self.get_session().query(MessageLog).filter(MessageLog.bot == self).order_by(
            MessageLog.timestamp.desc()).limit(n)

        return '\n'.join(map(str, log))

    def add_log(self, js, is_tech=False):
        log = MessageLog()
        log.bot_id = self.id
        log.bot = self
        if is_tech:
            log.direction = MessageLog.TECH
        elif js['message']['chat']['id'] == self.target_chat_id:
            log.direction = MessageLog.RESPONSE
            log.int_user_id = js['message']['from']['id']
            log.int_user_name = format_user(js['message']['from'])
        else:
            log.direction = MessageLog.REQUEST
            log.ext_user_id = js['message']['from']['id']
            log.ext_user_name = format_user(js['message']['from'])

        log.timestamp = js['message']['date']
        # self.content = js['message']['text']
        self.get_session().add(log)
        return log

    def attach_chat(self, chat_id):
        self.target_chat_id = chat_id
        return texts.ATTACHED

    def set_timezone(self, value):
        try:
            timezone = int(value)
        except ValueError as e:
            return e.__repr__()
        self.timezone = timezone
        return texts.TZ_SET + str(timezone)

    def set_greeting(self, value):
        self.start_text = value
        return value

    def forward_message(self, js):
        chat_id = js['message']['chat']['id']

        target_chat_id = self.target_chat_id
        if not target_chat_id:
            target_chat_id = self.owner_id

        result = {
            'method': 'forwardMessage',
            'chat_id': target_chat_id,
            'from_chat_id': chat_id,
            'message_id': js['message']['message_id'],
            "ok": True
        }
        if chat_id == self.target_chat_id:
            try:
                if 'reply_to_message' in js['message'] \
                        and "forward_date" in js['message']['reply_to_message']:
                    log = self.add_log(js)

                    if 'forward_from' in js['message']['reply_to_message']:
                        log.ext_user_name = format_user(
                            js['message']['reply_to_message']['forward_from'])
                        log.ext_user_id = result['chat_id'] = \
                            js['message']['reply_to_message']['forward_from']['id']
                    else:
                        log.ext_user_name = js['message']['reply_to_message']['forward_sender_name']
                        req_log: MessageLog = \
                            self.get_session().query(MessageLog).filter(MessageLog.bot == self,
                                                                        MessageLog.timestamp ==
                                                                        js['message'][
                                                                            'reply_to_message'][
                                                                            'forward_date']).first()
                        if req_log:
                            log.ext_user_id = result['chat_id'] = req_log.ext_user_id
                            log.ext_user_name = req_log.ext_user_name

            except Exception as e:
                result['method'] = 'sendMessage'
                result['text'] = str(e)
                result['reply_to_message_id'] = js['message']['message_id']
        else:
            self.add_log(js)

        return result