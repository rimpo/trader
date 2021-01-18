import telegram

class TelegramBot:
    def __init__(self, access_token: str):
        self.__bot = telegram.Bot(token=access_token)

    def send(self, message: str):
        self.__bot.send_message(chat_id=-462939300, text=message)
