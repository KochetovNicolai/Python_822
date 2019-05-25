from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Я телеграм-бот, который "
                          "показывает погоду в любом городе!")
    bot.send_message(chat_id=update.message.chat_id,
                     text="Комманды можно посмотреть написав /help\n")

def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Вы можете использовать такие комманды: \n"
                          "/help - возвращает список доступных комманд\n"
                          "/caps <arguments> - бот начинает писать капсом\n"
                          "/weather <city> - узнать погоду в городе, который вы передаете")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def Weather(bot, update, args):
    try:
        city = args[0]
        appid = "ad90afdfa34918d01559579762da4f03"
        result = requests.get("http://api.openweathermap.org/data/2.5/weather",
                              params={'q': city,
                                      'type': 'like', 'units': 'metric',
                                      'lang': 'ru', 'APPID': appid})
        data = result.json()
        bot.send_message(chat_id=update.message.chat_id,
                         text="conditions: {}".
                         format(data['weather'][0]['description']))
        bot.send_message(chat_id=update.message.chat_id,
                         text="Текущая температура: {} °C".format(data['main']['temp']))
        bot.send_message(chat_id=update.message.chat_id,
                         text="Минимальная температура: {} °C".format(data['main']['temp_min']))
        bot.send_message(chat_id=update.message.chat_id,
                         text="Максимальная температура: {} °C".format(data['main']['temp_max']))
        bot.send_message(chat_id=update.message.chat_id,
                         text="Давление: {}".format(data['main']['pressure']))
        bot.send_message(chat_id=update.message.chat_id,
                         text="Влажность: {}%".format(data['main']['humidity']))
        bot.send_message(chat_id=update.message.chat_id,
                         text="Скорость ветра: {} m/s".format(data['wind']['speed']))
    except BaseException:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Извините, не нашел такого города ")


def main():
    updater = Updater("589340845:AAGMfeMtTFUr1IirK6BUDoiV4hw_PZphXaQ")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler("caps", caps, pass_args=True))
    dp.add_handler(CommandHandler("weather", Weather, pass_args=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
