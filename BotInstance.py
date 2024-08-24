from datetime import timezone, timedelta, datetime
from model import BotModel, MessageLog, Blacklist
from sqlalchemy import func
import texts

MAX_DELAY = 10

def format_user(user):
    if 'username' in user:
        return '@' + user['username']
    else:
        result = []
        if 'first_name' in user:
            result.append(user['first_name'])
        if 'last_name' in user:
            result.append(user['last_name'])
        return ' '.join(result)


class BotInstance(BotModel):

    def tz(self):
        return timezone(timedelta(hours=self.timezone))

    def command(self, from_chat, text, from_user, quote, entities):
        if text.startswith('/start'):
            return self.start_text

        elif text == '/attach' and from_user['id'] == self.owner_id:
            return self.attach_chat(from_chat)

        elif text.startswith('/log') and from_chat in (self.owner_id, self.target_chat_id):
            return self.get_log_command(text, quote, entities)

        elif text.startswith('/dialogs') and from_chat in (self.owner_id, self.target_chat_id):
            return self.dialogs_command(text, entities)

        elif text.startswith('/ban') and from_chat in (self.owner_id, self.target_chat_id):
            return self.ban_command(quote, from_user)

        elif text.startswith('/unban') and from_chat in (self.owner_id, self.target_chat_id):
            return self.unban_command(text)

        elif text.startswith('/blacklist') and from_chat in (self.owner_id, self.target_chat_id):
            return self.blacklist_command()


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

    def get_log_command(self, text, quote, entities: list):
        n = 5
        if len(text) > 5:
            try:
                n = int(text[5:])
            except ValueError as e:
                return str(e)

        criteria = (MessageLog.bot == self)
        if quote and "forward_date" in quote:
            ext_user_id, ext_user_name = self.user_from_quote(quote)
            if ext_user_id:
                criteria = criteria & (MessageLog.ext_user_id == ext_user_id)
        log = self.get_session().query(MessageLog).filter(criteria).order_by(
            MessageLog.timestamp.desc()).limit(n)

        return MessageLog.format_log(log, entities)

    def dialogs_command(self, text, entities: list):
        n = 5
        if len(text) > 9:
            try:
                n = int(text[9:])
            except ValueError as e:
                return str(e)

        criteria = (MessageLog.bot == self)
        session = self.get_session()

        subquery = session.query(func.max(MessageLog.id).label('last')) \
            .filter(MessageLog.bot == self) \
            .group_by(MessageLog.ext_user_name) \
            .order_by(MessageLog.id.desc()) \
            .limit(n)

        query = session.query(MessageLog) \
            .filter(MessageLog.id.in_(subquery)) \
            .order_by(MessageLog.timestamp.desc())

        return MessageLog.format_log(query, entities)

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

    def ban_command(self, quote, from_user):
        if not (quote and "forward_date" in quote):
            return texts.SHOULD_REPLY
        ext_user_id, ext_user_name = self.user_from_quote(quote)

        if not (ext_user_id and ext_user_name):
            return "Failed"

        ban = Blacklist()
        ban.bot_id = self.id
        ban.bot = self
        ban.user_id = ext_user_id
        ban.name = ext_user_name
        ban.added_by = format_user(from_user)

        self.get_session().add(ban)

        return self.blacklist_command()

    def blacklist_command(self):
        if self.blacklist:
            return texts.BLACKLIST + '\n'.join(map(str, self.blacklist))
        else:
            return texts.EMPTY_BLACKLIST

    def unban_command(self, text):
        if not self.blacklist:
            return texts.EMPTY_BLACKLIST

        if len(text) > 7:
            try:
                unban_id = int(text[7:])
            except ValueError as e:
                return str(e) + '\n' + texts.ID_FOR_UNBAN
        else:
            return texts.ID_FOR_UNBAN

        result = texts.UNBANNED
        for user in self.blacklist:
            if user.user_id == unban_id:
                result += ' ' + str(user.name)
                self.get_session().delete(user)

        if result == texts.UNBANNED:
            return texts.ID_FOR_UNBAN

        return result


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
            if 'reply_to_message' in js['message'] \
                    and "forward_date" in js['message']['reply_to_message']:
                try:
                    log = self.add_log(js)
                    ext_user_id, log.ext_user_name = self.user_from_quote(js['message']['reply_to_message'])
                    if ext_user_id:
                        log.ext_user_id = result['chat_id'] = ext_user_id

                except Exception as e:
                    result['method'] = 'sendMessage'
                    result['text'] = str(e)
                    result['reply_to_message_id'] = js['message']['message_id']
            else:
                return {"ok": True}
        else:
            log = self.add_log(js)
            if self.blacklist and chat_id in (b.user_id for b in self.blacklist):
                result['chat_id'] = chat_id
                log.direction = MessageLog.DENIED
            elif "forward_date" in js['message']:
                log.int_user_id = js['message']['forward_date'] ## for searching

        return result

    def user_from_quote(self, quote):
        if 'forward_from' in quote:
            ext_user_name = format_user(quote['forward_from'])
        else:
            ext_user_name = quote['forward_sender_name']
        ext_user_id = None

        forward_date: int = quote['forward_date']

        req_log: MessageLog = self.get_session().query(MessageLog). \
            filter(MessageLog.bot == self,
                   MessageLog.timestamp == forward_date,
                   MessageLog.ext_user_name == ext_user_name).first()

        if not req_log:
            date: int = quote['date']
            req_log: MessageLog = self.get_session().query(MessageLog). \
                filter(MessageLog.bot == self,
                       MessageLog.int_user_id == forward_date,
                       MessageLog.timestamp <= date,
                       MessageLog.timestamp > date - MAX_DELAY
                       ).first()

        if req_log:
            ext_user_id = req_log.ext_user_id
            ext_user_name = req_log.ext_user_name

        return ext_user_id, ext_user_name
