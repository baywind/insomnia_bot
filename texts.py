DEFAULT_GREETING = '''Привет! Я простой и скромный бот-секретарь:
Перешлю твои сообщения в чатик, а когда ответят, перешлю тебе обратно ответ.'''

UNKNOWN_COMMAND = '''Не пытайся давать мне команды, я всё равно не пойму =(
Я умею только пересылать сообщения туда-обратно'''


NOPE = 'Так не работает. Можно только отвечать на пересланные сообщения.'


REGISTERED = '''Зарегистрирован новый бот под именем: %s.

Теперь добавьте его в целевой чат и выполните там команду /attach

Другие команды настройки доступны по команде /help'''


UNKNOWN_BOT = '''Этот бот ещё не зарегистрирован. Он не станет ничего делать.
Владелец бота должен выполнить команду /register'''


ERROR_CREATING = 'Не удалось зарегистрировать бота: '


ADM_HELP = '''Команды бота:

/greeting {текст} — установить приветственное сообщение для новых пользователей, \
 которое выводится при выполнении команды /start

/timezone {число} — установить временную зону для вывода лога последних действий (по умолчанию +3)

/attach — выполняется в целевом чате, чтобы бот пересылал в него сообщения

/log {число} — выводит указанное количество последних пересланных сообщений (по умолчанию 5). \
можно применять в целевом чате или в личном чате с администратором.
Если отправить команду /log в ответ на сообщение, пересланное ботом, \
то будет выведена история переписки с автором этого сообщения.

/dialogs {число} — выводит указанное количество последних контрагентов, \
с которыми велась переписка через бота (по умолчанию 5).

/ban — в ответ на сообщение нежелательного пользователя в чате, чтобы больше его сообщения не пересылались
/blacklist — чтобы посмотреть список забаненых
/unban с идентификатором из черного списка, чтобы снять блокировку
'''

TZ_SET = 'TimeZone is set to: '

ATTACHED = '''Выполнено присоединение!
Теперь бот будет пересылать все сообщения в этот чат'''

CHAT_HELP = '''Бот пересылает все сообщения в этот чат. \
Ответы на сообщения пересылает из чата обратно автору.

Посмотреть последние собщения можно с помощью команды /log
Если отправить в ответ на сообщение, покажет историю переписки с автором.

Посмотреть последних собеседников — командой /dialogs
'''

SHOULD_REPLY = 'Эта команда может быть выполнена только в ответ на сообщение от бота'

BANNED = 'Пользователь заблокирован'

UNBANNED = 'Исключен из черного списка:'

BLACKLIST = 'Актуальный черный список:\n'

EMPTY_BLACKLIST = "Черный список пуст. " \
    "Используйте команду /ban в ответ на сообщение, чтобы добавить пользователя в черный список"

ID_FOR_UNBAN = "Укажите идентификатор из черного списка (/blacklist) чтобы разблокировать"

