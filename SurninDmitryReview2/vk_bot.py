from helpful_functions import Functions


class VkBot:

    def __init__(self, user_id):
        print("\nНовая команда")

        self._flag = None
        self._USER_ID = user_id
        self._USERNAME = Functions.get_user_name_from_vk_id(Functions, user_id)
        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "ПОКА", "ДАТА"]

    def new_message(self, message, flag):

        self._flag = flag

        if self._flag == 'weather':
            self._flag = None
            return Functions.get_weather(str(message)), self._flag

        elif message.upper().startswith(self._COMMANDS[0]):
            return "Здравствуй, {}!".format(self._USERNAME), self._flag

        elif message.upper() == self._COMMANDS[1]:
            self._flag = 'weather'
            return "Город назовите, погоду в котором узнать хотите вы(языке на русском)", self._flag

        elif message.upper() == self._COMMANDS[2]:
            return Functions.get_time(), self._flag

        elif message.upper().startswith(self._COMMANDS[3]):
            return "Свидания до, {}!".format(self._USERNAME), self._flag

        elif message.upper() == self._COMMANDS[4]:
            return Functions.get_date(), self._flag

        else:
            return "Вас не понимаю я", self._flag
