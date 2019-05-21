import telebot
import requests
import json


class Manager:
    def __init__(self):
        with open('configs.json') as f:
            configs = json.load(f)

        self.bot = telebot.TeleBot(configs['token'])
        self.options = {'app_id': configs['app_id'], 'app_key': configs['app_key']}
        self.search_options_reset()

    def search_options_reset(self, step=5):
        self.options['q'] = None
        self.options['from'] = 0
        self.options['to'] = step
        self.options['excluded'] = None
        self.options['time'] = None

    def search_boards_next(self, step=5):
        self.options['from'] = self.options['to'] - 1
        self.options['to'] = self.options['to'] + step - 1

    def handle(self):
        M = self
        @M.bot.message_handler(commands=['start'])
        def handle_start(message):
            M.bot.send_message(message.chat.id, 'Hello! I\'ll help you to find the best food recipes')

        @M.bot.message_handler(commands=['help'])
        def handle_start(message):
            M.bot.send_message(message.chat.id, 'Write \'Cooking-time\' for start!\n'
                                              'When you choose all options write \'Search\' to look at the result')

        @M.bot.message_handler(content_types=['text'], regexp="Cooking-time")
        def handle_eat(message):
            M.bot.send_message(message.chat.id, "Let\'s go! What are you going to find?")
            M.bot.register_next_step_handler(message, get_query)

        def get_query(message):

            msg = message.text
            msg.split(', ')
            ' '.join(msg)

            M.options['q'] = msg

            keyboard = telebot.types.InlineKeyboardMarkup()

            key_ex = telebot.types.InlineKeyboardButton(text='Exclude Ingredients', callback_data='exclude')
            keyboard.add(key_ex)
            key_time = telebot.types.InlineKeyboardButton(text='Set maximum cooking time', callback_data='time')
            keyboard.add(key_time)
            M.bot.send_message(message.chat.id, 'You can choose any extra options:', reply_markup=keyboard)

        @M.bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            if call.data == "exclude":
                M.bot.send_message(call.message.chat.id, "Which ingredients do you want to exclude?")
                M.bot.register_next_step_handler(call.message, get_exclude)
            elif call.data == "time":
                M.bot.send_message(call.message.chat.id, "What max time do you want to cook?")
                M.bot.register_next_step_handler(call.message, get_time)

        def get_exclude(message):
            msg = message.text.split(', ')
            query = []
            for line in msg:
                query.append(line)
            if len(query) == 1:
                M.options['excluded'] = query[0]
            else:
                M.options['excluded'] = query
            M.bot.send_message(message.chat.id, 'OK')

        def get_time(message):
            msg = message.text.split(' ')
            if len(msg) <= 1:
                M.options['time'] = str(int(msg[0]))
                M.bot.send_message(message.chat.id, 'OK')
            elif msg[1].lower() == 'minutes' or msg[1].lower() == 'minute' or msg[1].lower() == 'min':
                M.options['time'] = str(int(msg[0]))
                M.bot.send_message(message.chat.id, 'OK')
            elif msg[1].lower() == 'hours' or msg[1].lower() == 'hour':
                time = float(msg[0])
                mins = int((int(time * 10) % 10) * 6)
                mins += int(time) * 60
                M.options['time'] = str(mins)
                M.bot.send_message(message.chat.id, 'OK')
            else:
                M.bot.send_message(message.chat.id, 'Something wrong')

        # def get_dish(message):
        #     msg = message.text.split(', ')
        #     global options
        #     for line in msg:
        #         line = line.split(' ')
        #         '+'.join(line)
        #         options['dishType'] += '&dishType={}'.format(line[0])
        #     bot.send_message(message.chat.id, 'OK')
        # к сожалению, эта опция у API работает только с платной подпиской

        @M.bot.message_handler(content_types=['text'], regexp="Search")
        def handle_search(message):
            M.bot.send_message(message.chat.id, "A minute...")
            search(message)

        @M.bot.message_handler(content_types=['text'])
        def handle_search(message):
            M.bot.send_message(message.chat.id, "Sounds interesting")

        def display_results(message, info, count):
            for i in range(count):
                recipe = info[i]['recipe']
                M.bot.send_message(message.chat.id, recipe['label'] + '\n' + recipe['url'])
                M.bot.send_photo(message.chat.id, recipe['image'])

                M.bot.send_message(message.chat.id, 'Total time: ' + str(int(recipe['totalTime'])) + ' minutes')
                answer = 'Ingredients:\n'
                for j in recipe['ingredientLines']:
                    answer += '> ' + j + '\n'
                M.bot.send_message(message.chat.id, answer)

        def search(message, step=5):
            if message.text.lower() == 'yes' or message.text.lower() == 'search':

                if len(M.options['q']) == 0:
                    M.bot.send_message(message.chat.id, 'Whoops, no data for search((')
                    M.search_options_reset()
                    return

                try:
                    info = requests.get('https://api.edamam.com/search', params=M.options)
                except Exception:
                    M.bot.send_message(message.chat.id, 'Whoops, request is incorrect. Go again')
                    M.search_options_reset()
                    return

                try:
                    info = info.json()['hits']
                except Exception:
                    M.bot.send_message(message.chat.id, 'Whoops, something wrong on server. Go again')
                    M.search_options_reset()
                    return

                # print(M.options)
                # info = requests.get('https://api.edamam.com/search', params=M.options)
                # info = info.json()['hits']

            # если нашлись все step рецептов - выдадим все, кроме одного, и спросим, нужно ли найти ещё рецепты
                if len(info) == step:
                    display_results(message, info, len(info) - 1)
                    M.bot.send_message(message.chat.id, 'I have moooore suitable recipes! Show? [Yes/No]')
                    M.search_boards_next()
                    M.bot.register_next_step_handler(message, search)
                else:
                    display_results(message, info, len(info))
                    M.search_options_reset()

            else:
                M.bot.send_message(message.chat.id, 'Bye...')
                M.search_options_reset()

        M.bot.polling()
