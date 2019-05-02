from telebot import TeleBot
from bot_logic import BotLogic

token = "854886337:AAHIgbDJBSKgIWK_9TvjCDC9ScvdBxu0650"
bot = TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello!")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''Доступные команды:\n
    Find film - searches info about the film in IMDB\n
    Add film in watched list - adds film from IMDB in your watched films list\n
    Add film in wish list - adds film from IMDB in your wanted to watch film list\n
    Show my watched list - shows your watched list\n
    Show my wish list - shows list of films you want to watch''')


@bot.message_handler(content_types='text')
def handle_text(message):
    bot.send_message(message.chat.id, BotLogic().handle_text_message(message.text, message.from_user.id))
