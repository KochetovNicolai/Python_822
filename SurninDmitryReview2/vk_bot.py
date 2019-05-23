from helpful_functions import Functions


class VkBot:

    def __init__(self, user_id):
        print("\nНовая команда")

        self._flag = None
        self._message = 'None'
        self._USER_ID = user_id
        self._USERNAME = Functions.get_user_name_from_vk_id(Functions, user_id)
        self._Commands = {'ПРИВЕТ': self.hello_func,
                          'ПОГОДА': self.weather,
                          'ВРЕМЯ': self.time,
                          'ДАТА': self.date,
                          'ПОКА': self.bye_func,
                          'КОТ': self.cat_fact}

    def new_message(self, message, flag):

        self._flag = flag
        self._message = message.upper()

        if self._flag == 'weather':
            return self._Commands['ПОГОДА']()

        elif self._message.startswith('ПРИВЕТ'):
            return self._Commands['ПРИВЕТ']()

        elif self._message.startswith('ПОКА'):
            return self._Commands['ПОКА']()

        elif self._message in self._Commands.keys():
            return self._Commands[self._message]()

        else:
            return "Вас не понимаю я", self._flag

    def hello_func(self):
        return "Здравствуй, {}!".format(self._USERNAME), self._flag

    def weather(self):
        if self._flag is None:
            self._flag = 'weather'
            return "Город назовите, погоду в котором узнать хотите вы (языке на русском)", self._flag
        else:
            self._flag = None
            return Functions.get_weather(str(self._message.lower())), self._flag

    def time(self):
        return Functions.get_time(), self._flag

    def date(self):
        return Functions.get_date(), self._flag

    def bye_func(self):
        return "Свидания до, {}!".format(self._USERNAME), self._flag

    def cat_fact(self):
        return Functions.get_fact(), self._flag
