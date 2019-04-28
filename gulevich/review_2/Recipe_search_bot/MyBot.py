import telebot
import requests


app_key = 'a2e39fa2eabb2c12a2e37d7de0dbb566'
app_id = '3c769ea5'
token = '814973297:AAEfq0OWImkZkWxuHX2foamlURQQsUyd06A'

bot = telebot.TeleBot(token)

options = {'query': '', 'excluded': '', 'time': ''}
boards = [0, 0]


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Hello! I\'ll help you to find the best food recipes')


@bot.message_handler(commands=['help'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Write \'Cooking-time\' for start!\n'
                                      'When you choose all options write \'Search\' to look at the result')


@bot.message_handler(content_types=['text'], regexp="Cooking-time")
def handle_eat(message):
    bot.send_message(message.chat.id, "Let\'s go! What are you going to find?")
    bot.register_next_step_handler(message, get_query)


def get_query(message):
    global options

    msg = message.text
    msg.split(', ')
    '%2B'.join(msg)

    options['query'] = msg

    keyboard = telebot.types.InlineKeyboardMarkup()

    key_ex = telebot.types.InlineKeyboardButton(text='Exclude Ingredients', callback_data='exclude')
    keyboard.add(key_ex)
    key_time = telebot.types.InlineKeyboardButton(text='Set maximum cooking time', callback_data='time')
    keyboard.add(key_time)
    bot.send_message(message.chat.id, 'You can choose any extra options:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "exclude":
        bot.send_message(call.message.chat.id, "Which ingredients do you want to exclude?")
        bot.register_next_step_handler(call.message, get_exclude)
    elif call.data == "time":
        bot.send_message(call.message.chat.id, "What max time do you want to cook?")
        bot.register_next_step_handler(call.message, get_time)


def get_exclude(message):
    msg = message.text.split(', ')
    global options
    for line in msg:
        line = line.split(' ')
        '%2B'.join(line)
        options['excluded'] += '&excluded={}'.format(line[0])
    bot.send_message(message.chat.id, 'OK')


def get_time(message):
    msg = message.text.split(' ')
    global options

    if msg[1].lower() == 'minutes' or msg[1].lower() == 'minute' or msg[1].lower() == 'min':
        options['time'] += '&time={}'.format(str(int(msg[0])))
        bot.send_message(message.chat.id, 'OK')
    elif msg[1].lower() == 'hours' or msg[1].lower() == 'hour':
        time = float(msg[0])
        mins = int((int(time*10) % 10)*6)
        mins += int(time) * 60
        options['time'] += '&time={}'.format(str(mins))
        bot.send_message(message.chat.id, 'OK')
    else:
        bot.send_message(message.chat.id, 'Something wrong')


# def get_dish(message):
#     msg = message.text.split(', ')
#     global options
#     for line in msg:
#         line = line.split(' ')
#         '+'.join(line)
#         options['dishType'] += '&dishType={}'.format(line[0])
#     bot.send_message(message.chat.id, 'OK')


@bot.message_handler(content_types=['text'])
def handle_search(message):
    bot.send_message(message.chat.id, "Sounds interesting")


@bot.message_handler(content_types=['text'], regexp="Search")
def handle_search(message):
    bot.send_message(message.chat.id, "A minute...")
    search_boards_reset()
    search(message)


def search_options_reset():
    global options
    for key in options.keys():
        options[key] = ''


def search_boards_reset(step=5):
    global boards
    boards[0] = 0
    boards[1] = step


def search_boards_next(step=5):
    global boards
    boards[0] = boards[1] - 1
    boards[1] = boards[1] + step - 1


def display_results(message, info, count):
    for i in range(count):
        recipe = info[i]['recipe']
        bot.send_message(message.chat.id, recipe['label'] + '\n' + recipe['url'])
        bot.send_photo(message.chat.id, recipe['image'])

        bot.send_message(message.chat.id, 'Total time: ' + str(int(recipe['totalTime'])) + ' minutes')
        answer = 'Ingredients:\n'
        for j in recipe['ingredientLines']:
            answer += '> ' + j + '\n'
        bot.send_message(message.chat.id, answer)


def form_api():
    global options
    global boards
    api = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(options['query'], app_id, app_key)
    api += '&from=' + str(boards[0])
    api += '&to=' + str(boards[1])
    api += options['excluded']
    api += options['time']
    return api


def search(message, step=5):
    global options
    global boards

    if message.text.lower() == 'yes' or message.text.lower() == 'search':

        if len(options['query']) == 0:
            bot.send_message(message.chat.id, 'Whoops, no data for search((')
            search_options_reset()
            return

        api = form_api()
        #print(api)

        try:
            info = requests.get(api)
        except Exception:
            bot.send_message(message.chat.id, 'Whoops, request is incorrect. Go again')
            search_boards_reset()
            search_options_reset()
            return
        # info = requests.get(api)
        info = info.json()['hits']

    # если нашлись все step рецептов - выдадим все, кроме одного, и спросим, нужно ли найти ещё рецепты
        if len(info) == step:
            display_results(message, info, len(info) - 1)
            bot.send_message(message.chat.id, 'I have moooore suitable recipes! Show? [Yes/No]')
            search_boards_next()
            bot.register_next_step_handler(message, search)
        else:
            display_results(message, info, len(info))
            search_options_reset()
            search_boards_reset()

    else:
        bot.send_message(message.chat.id, 'Bye...')
        search_boards_reset()
        search_options_reset()


bot.polling()
