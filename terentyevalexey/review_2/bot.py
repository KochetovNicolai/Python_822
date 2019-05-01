import requests
from html import unescape
from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Filters
from TOKEN import BOT_TOKEN
# TOKEN SENT IN TELEGRAM


def start(bot: Bot, update: Update):
    username = update.message.from_user['first_name']
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Easy', callback_data='easy'),
         InlineKeyboardButton('Medium', callback_data='medium'),
         InlineKeyboardButton('Hard', callback_data='hard')],
    ])
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Не очень умный бот готов задавать вам вопросы.\n" +
             f"Справитесь ли вы с ними, {username}?\n" +
             "Выберите сложность",
        reply_markup=keyboard,
    )


def talk(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='qq',
    )


def ask(bot: Bot, update: Update):
    query = update.callback_query

    question = requests.get(
        f"http://opentdb.com/api.php?amount=1&difficulty={query.data}").json()
    if question['response_code'] != 0:
        return
    question = question['results'][0]
    query.edit_message_text(text=unescape(question['question']))


def main():
    bot = Bot(
        token=BOT_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler('start', start)
    talk_handler = MessageHandler(Filters.text, talk)
    callback_handler = CallbackQueryHandler(ask)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(talk_handler)
    updater.dispatcher.add_handler(callback_handler)

    updater.start_polling()
    print(7)
    updater.idle()
    print(8)


if __name__ == '__main__':
    main()
