# Forwarder bot

Это бот для Telegram, предназначенный для пересылки сообщений сторонних пользователей в закрытый чат команды и возвращения ему ответов из чата.

Бот запущен и используется для команд некоторых направлений при организации фестиваля Бессонница.
Например, можно задать вопрос по набору волонтёров в https://t.me/insomnia_volunteers_bot

Бот построен на использовании webhook в Telegram API без использования специальных библиотек-обёрток.
Подробнее: https://core.telegram.org/bots/webhooks

## Принцип работы

Программа представляет собой движок, в котором можно регистрировать ботоы для разных команд.

Любой пользователь Telegram может подключиться к боту.
Сообщения, которые пользователь отправит боту пересылаются в закрытый чат команды, которой принадлежит этот бот.

Любой из участников чата может ответить на сообщение (стандартным способом для Telegram), и бот перешлёт этот ответ автору оригинального сообщения.

Таким образом внешнему пользователю не нужно решать, к кому именно из команды обращаться — на его вопрос может ответить любой представитель из закрытого чата.
Предварительно ответ можно обсудить внутри команды, а вопрошающему отправить уже согласованный командой «вердикт».

## Как запустить бота

Инструкция предполагает использование туннеля ngrok

1.  зарегистрировать своего бота с помощью [@BotFather](https://t.me/botfather)

2.  отредактировать файл webhook_setter.py:
    * вставить значение API_KEY, который выдал BotFather
    * вставить зарегистрированное имя бота
    * вставить url, на котором доступен сервис бота
    (например, доступный через ngrok. обязательно **https**)

3.  выполнить webhook_setter.py

    Проверить успешность регистрации бота и webhook можно с помощью logger_server.py — он просто выдаёт в консоль все обращения.
    Если направить на него webhook, можно видеть json-структуру запросов от Telegram при обращенях к боту.
    
    _Менять url-адрес webhook можно сколько угодно раз, используя webhook_setter.py_
    
4.  зарегистрировать бота в сервисе и стать его администратором — для этого выполнить команду /register

5.  добавить бота в группу в Telegram

5.  назначить эту группу целевой для бота —  для этого выполнить в группе команду /attach

6.  проверить работу бота:
    * написать сообщение боту от имени любого пользователя
    * убедиться, что это сообщение появилось в группе
    * ответить на сообщение в группе
    * убедиться, что ответное сообщение отправилось пользователю
    
## Другие возможности бота

Просмотреть историю пересылок можно командой /log .
Команда выполняется любым пользователем в целевой группе либо администратором в личных сообщениях с ботом.

Администратор может настраивать параметры бота:
* Приветственное сообщение
* часовой пояс для отображения времени в логе

Подсказку по доступным командам для администратора можно вывести командой /help (или любой неизвестной командой)

## Файлы в дистрибутиве:
Логика работы программы представлена в 4х файлах:
* flask_app.py — основное приложение, обеспечивающее сервис
* BotInstance.py — реализация бизнес-логики бота
* model.py — ORM-модель, описывающая хранение настроек бота и истории пересылок
* texts.py — текстовые сообщения, которые выдаёт бот

Вспомогательные файлы
* webhook_setter.py — скрипт для установки боту адреса webhook
* logger_server.py — простейший сервис для проверки правильности подключения
* requirements.txt — список используемых библиотек
* README.md — это описание

Файл базы данных **db.sqlite** создаётся автоматически при первом запуске сервиса.