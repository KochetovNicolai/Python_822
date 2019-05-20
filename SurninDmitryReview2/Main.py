import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
from configparser import ConfigParser
from vk_bot import VkBot


flag = None
identify = None
parser = ConfigParser()
parser.read('config.ini')
my_token = parser.get('token', 'first_token')


def write_msg(user_id, message):
    # vk.method('messages.send', {'user_id': user_id, 'message': message})
    random_id = randint(1, 100000)
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': random_id
    })


token = my_token
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

print("Bot have been started")
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            print('New message:')
            print(f'For me by: {event.user_id}', end='')

            bot = VkBot(event.user_id)

            message, flag = bot.new_message(event.text, flag)
            write_msg(event.user_id, message)
            print('Text: ', event.text)

#необходимо писать название города на русском языке
#но существует защита от неправильного или несуществующего города
