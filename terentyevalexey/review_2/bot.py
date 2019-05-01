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
import random


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
        text="Not the cleverest bot is ready to ask you questions.\n" +
             f"Can you handle them, {username}?\n" +
             "Choose the difficulty",
        reply_markup=keyboard,
    )


def question(bot: Bot, update: Update):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Easy', callback_data='easy'),
         InlineKeyboardButton('Medium', callback_data='medium'),
         InlineKeyboardButton('Hard', callback_data='hard')],
    ])
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Choose the difficulty",
        reply_markup=keyboard,
    )


def talk(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Do you want a question?',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('Yes', callback_data=random.choice(
                ['easy', 'medium', 'hard'])), ]])
    )


def ask(bot: Bot, update: Update):
    query = update.callback_query

    question_req = requests.get(
        f"http://opentdb.com/api.php?amount=1&difficulty={query.data}").json()
    if question_req['response_code'] != 0:
        return
    question_req = question_req['results'][0]

    # answers choice keyboard
    answers = question_req['incorrect_answers']
    right_answer = question_req['correct_answer']
    answers.append(right_answer)

    random.shuffle(answers)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(unescape(answer), callback_data=(
                (
                    'correct' if answer == right_answer else 'incorrect') + unescape(
            right_answer))),
         ] for answer in answers
    ])

    query.edit_message_text(
        text=unescape(question_req['question']),
        reply_markup=keyboard,
    )


def correct_answer(bot: Bot, update: Update):
    query = update.callback_query
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Easy', callback_data='easy'),
         InlineKeyboardButton('Medium', callback_data='medium'),
         InlineKeyboardButton('Hard', callback_data='hard')],
    ])
    query.edit_message_text(
        text=unescape(query.message.text + '\nIndeed!' +
                      f'\n{query.data[7::]} - is the right answer!' +
                      '\nDo you want a next question?'),
        reply_markup=keyboard,
    )


def incorrect_answer(bot: Bot, update: Update):
    query = update.callback_query
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Easy', callback_data='easy'),
         InlineKeyboardButton('Medium', callback_data='medium'),
         InlineKeyboardButton('Hard', callback_data='hard')],
    ])
    query.edit_message_text(
        text=unescape(query.message.text + '\nNo, you are wrong!' +
                      f'\n{query.data[9::]} - is the correct answer.' +
                      '\nMaybe, the next question will be easier?'),
        reply_markup=keyboard,
    )


def callback_handle(bot: Bot, update: Update):
    query = update.callback_query
    if query.data in ['easy', 'medium', 'hard']:
        ask(bot, update)
    elif query.data.startswith('correct'):
        correct_answer(bot, update)
    elif query.data.startswith('incorrect'):
        incorrect_answer(bot, update)


def question_create(bot: Bot, update: Update):
    difficulty = update.message.text.split(None, 1)[0][1::]
    question_req = requests.get(
        f"http://opentdb.com/api.php?amount=1&difficulty={difficulty}").json()
    if question_req['response_code'] != 0:
        return
    question_req = question_req['results'][0]
    # answers choice keyboard
    answers = question_req['incorrect_answers']
    right_answer = question_req['correct_answer']
    answers.append(right_answer)

    random.shuffle(answers)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(unescape(answer), callback_data=(
                (
                    'correct' if answer == right_answer else 'incorrect') + unescape(
            right_answer))),
         ] for answer in answers
    ])

    bot.send_message(
        chat_id=update.message.chat_id,
        text=unescape(question_req['question']),
        reply_markup=keyboard,
    )


def main():
    bot = Bot(
        token=BOT_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler('start', start)
    new_handler = CommandHandler('new', question)
    difficulty_handler = CommandHandler(['easy', 'medium', 'hard'],
                                        question_create)
    talk_handler = MessageHandler(Filters.text, talk)
    callback_handler = CallbackQueryHandler(callback_handle)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(new_handler)
    updater.dispatcher.add_handler(talk_handler)
    updater.dispatcher.add_handler(difficulty_handler)
    updater.dispatcher.add_handler(callback_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
