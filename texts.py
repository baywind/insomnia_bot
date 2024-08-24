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