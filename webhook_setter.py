import requests

API_KEY = "what you get from @BotFather"
BOT_NAME = 'username_of_your_bot'

MY_SERVICE_URL = f"https://application.listening.url/{BOT_NAME}"

result = requests.get(f"https://api.telegram.org/bot{API_KEY}/setWebhook",
                      {'url': MY_SERVICE_URL})

print(result, result.text)
