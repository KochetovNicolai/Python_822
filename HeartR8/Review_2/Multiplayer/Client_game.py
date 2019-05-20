import arcade
from Multiplayer import client_field, Client_UI, multiplayer_classes
from threading import Thread
import threading
import os
import pickle


class MyGame(arcade.Window):
    def __init__(self, socket):
        # pygame.mixer.init()
        # pygame.mixer.music.load('../Background_music.wav')
        # pygame.mixer.music.play(-1)
        super().__init__(title="School battle", resizable=True)
        arcade.set_background_color(arcade.color.WHITE)
        self.fraction = ""
        self.sock = socket
        self.button_list = None
        self.unit_list = []
        self.highlighted_cells = []
        self.background = None
        self.frac_list = [multiplayer_classes.CriminalFraction,
                          multiplayer_classes.MajorsFraction,
                          multiplayer_classes.PartyFraction,
                          multiplayer_classes.BotansFraction]
        self.fraction_choose_buttons_list = []
        self.create_unit_button_list = []
        self.fraction_names = ['Преступники',
                               'Мажоры',
                               'Тусовщики',
                               'Ботаны']

        self.fractions_units_names = [['Быдлан', 'Барыга', 'Оффник', 'Зек'],
                                      ['Подсосник', 'Показушник', 'Мажор', 'Главный мажор'],
                                      ['Фан', 'Модник', 'Стрелочник', 'Миша'],
                                      ['Доходяга', 'Отличник', 'Тупой друг', 'Любимчик']]

        self.frac_choose_but_between_center = 50
        self.frac_choose_but_x_coef = 0.5
        self.frac_choose_but_y_coef = 0.5
        self.upper_than_frac_ch_but = 150

        self.start_menu_buttons_amount = 4

        self.add_money = 20

        self.information_txt_x_coef = 0.6
        self.information_txt_y_coef = 0.75

        self.delta_size_pix = 5
        self.unit_but_x_coef = 0.85
        self.unit_but_y_coef = 0.75
        self.unit_but_between = 100
        self.units_amount = 4
        self.unit_but_size_x = 200
        self.unit_but_size_y = 60

        self.left_menu_but_pos = 120
        self.delta_menu_but = 250
        self.bottom_menu_but = 30
        self.menu_but_size_x = 200
        self.menu_but_size_y = 50

        self.game_started = False
        self.number_of_players = 0
        self.base_dict = {}

    def setup(self):
        self.button_list = []
        print(os.getcwd())
        # self.background = arcade.load_texture("../BG2.jpg")

        quit_button = Client_UI.StartTextButton(self.left_menu_but_pos, self.bottom_menu_but,
                                                self.close_program, "Выход",
                                                self.menu_but_size_x, self.menu_but_size_y)
        self.button_list.append(quit_button)
        
        for i in range(self.units_amount):
            create_unit_button = Client_UI.CreateUnitButton(self.width * self.unit_but_x_coef,
                                                            self.height * self.unit_but_y_coef - i * self.unit_but_between,
                                                            self.unit_but_size_x,
                                                            self.unit_but_size_y,
                                                            self.create_unit,
                                                            self.fractions_units_names[0][0],
                                                            '')
            self.create_unit_button_list.append(create_unit_button)
        
        for i in range(len(self.frac_list)):
            self.fraction_choose_buttons_list.append(
                Client_UI.FractionChooseButton(self.width * self.frac_choose_but_x_coef,
                                               self.height * self.frac_choose_but_y_coef + self.frac_choose_but_between_center * 2 - self.frac_choose_but_between_center * i,
                                               self.create_fraction,
                                               self.fraction_names[i],
                                               self.fraction_names[i]))
        thr = Thread(target=self.recieve_messages)
        thr.start()
        print(threading.enumerate())

    def on_draw(self):
        arcade.start_render()
        if self.game_started:
            self.field.draw_field()
            self.draw_bases()
            self.draw_buttons(self.create_unit_button_list)
            # if self.game_started:
            #     for button in self.button_list:
            #         button.draw()
            # else:
            #     for button in range(len(self.button_list) - self.start_menu_buttons_amount):
            #         self.button_list[button].draw()
            #
            # for button in self.unit_list:
            #     button.draw()
            #
            # if self.game_started:
            #     for i in range(len(self.button_list) - self.start_menu_buttons_amount, len(self.button_list)):
            #         self.button_list[i].action_function = self.player_list[self.turn].create_unit
            #         temporary = self.player_list[self.turn].name_units[i - len(self.button_list) + self.start_menu_buttons_amount]
            #         self.button_list[i].unit_type = temporary
            #         temporary = self.player_list[self.turn].name_units_text[i - len(self.button_list) + self.start_menu_buttons_amount]
            #         self.button_list[i].text = temporary
            #         temporary = self.player_list[self.turn].base.place
            #         self.button_list[i].base_position = temporary
            #
            # for button in self.highlighted_cells:
            #     button.draw()

        else:
            for button in self.fraction_choose_buttons_list:
                button.draw()
                text = Client_UI.Text('Выберите фракцию:',
                                      self.height * self.frac_choose_but_x_coef + self.upper_than_frac_ch_but,
                                      self.width * self.frac_choose_but_y_coef)
                text.draw_text()

    def update(self, delta_time):
        pass
        # self.sock.setblocking(False)
        # message = self.sock.recv(1024)
        # message.decode()
        # if message == "start_game":
        #     self.fraction_choose_buttons_list = []

    def on_mouse_press(self, x, y, button, key_modifiers):
        Client_UI.check_mouse_press_for_buttons(x, y, self.button_list)
        Client_UI.check_mouse_press_for_buttons(x, y, self.create_unit_button_list)
        Client_UI.check_mouse_press_for_buttons(x, y, self.unit_list)
        Client_UI.check_mouse_press_for_buttons(x, y, self.highlighted_cells)
        Client_UI.check_mouse_press_for_buttons(x, y, self.fraction_choose_buttons_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        Client_UI.check_mouse_release_for_buttons(x, y, self.button_list)
        Client_UI.check_mouse_release_for_buttons(x, y, self.create_unit_button_list)
        Client_UI.check_mouse_release_for_buttons(x, y, self.unit_list)
        Client_UI.check_mouse_release_for_buttons(x, y, self.highlighted_cells)
        Client_UI.check_mouse_release_for_buttons(x, y, self.fraction_choose_buttons_list)

    def draw_buttons(self, button_list):
        for button in button_list:
            button.draw()

    def draw_bases(self):
        delta_size_pix = 5
        for i in self.base_dict:
            arcade.draw_rectangle_filled(
                self.base_dict[i][0] * self.field.cell_size + self.field.left_border - self.field.cell_size // 2,
                self.base_dict[i][1] * self.field.cell_size + self.field.bottom_border - self.field.cell_size // 2,
                self.field.cell_size - delta_size_pix,
                self.field.cell_size - delta_size_pix,
                color=arcade.color.GRAY_ASPARAGUS)
            base_owner = Client_UI.Text(i,
                                        self.base_dict[i][1]
                                        * self.field.cell_size + self.field.bottom_border - self.field.cell_size // 2,
                                        self.base_dict[i][0]
                                        * self.field.cell_size + self.field.left_border - self.field.cell_size // 2)
            base_owner.draw_text()

    def create_unit(self, unit_type):
        answer = ""
        while answer == "":  # пока не получили ответ от сервера
            self.sock.send(bytes("create unit {unit_type}", "UTF-8"))  # отправляем запрос
            print('sent request to create "{}"...'.format(unit_type))
            try:
                answer = self.sock.recv(1024)  # ожидаем ответа
                answer = answer.decode()  # декодируем полученные данные
            except:  # если не получили ответа отправляем запрос повторно
                pass
        print("received answer")

    def ask_for(self, request):
        sth = 0
        while sth == 0:  # пока не получили ответ от сервера
            self.sock.send(bytes(request, "UTF-8"))  # отправляем запрос
            print('sent request "{}"...'.format(request))
            try:
                sth = self.sock.recv(1024)  # ожидаем ответа
                sth = int(sth.decode())  # декодируем полученные данные
            except:  # если не получили ответа отправляем запрос повторно
                pass
        print("received answer")
        return sth

    def recv_place_of_bases(self):
        base_dict = {}
        while base_dict == {}:  # пока не получили ответ от сервера
            self.sock.send(bytes("place of bases", "UTF-8"))  # отправляем запрос
            print('sent request "{}"...'.format("place of bases"))
            try:
                base_dict = self.sock.recv(1024)  # ожидаем ответа
                base_dict = pickle.loads(base_dict)  # декодируем полученные данные
            except:  # если не получили ответа отправляем запрос повторно
                pass
        print("received answer")
        return base_dict

    def start_game(self):
        self.fraction_choose_buttons_list = []

        field_size = self.ask_for("get field size")
        self.field = client_field.GameField(min(self.width, self.height) // 4 * 3, field_size)  # создаем игровое поле

        number_of_players = self.ask_for("number of players")  # запрашивем количество игроков в сессии
        self.number_of_players = number_of_players

        self.base_dict = self.recv_place_of_bases()  # запрашиваем местоположение баз
        print(self.base_dict)

        for i, button in enumerate(self.create_unit_button_list):  # передаем в кнопки соответствующие название юнитов
            button.text = self.fractions_units_names[self.fraction_names.index(self.fraction)][i]

        self.game_started = True

    def run_command(self, message):
        if message == "start game":
            self.start_game()

    def recieve_messages(self):
        while True:
            self.sock.setblocking(0)
            self.sock.settimeout(0.1)
            message = ""
            try:
                message = self.sock.recv(1024).decode()
                print('received message "{}"'.format(message))
            except:
                pass
            if message != "":
                self.run_command(message)
            self.sock.setblocking(1)

    def get_fractions_chosen(self):
        self.sock.send(bytes(self.get_fractions_chosen.__name__, "UTF-8"))

    def close_program(self):
        self.close()

    def create_fraction(self, fraction):
        print(str(fraction))
        self.sock.send(bytes(str(fraction), "UTF-8"))
        self.fraction = fraction
        # message = self.sock.recv(1024).decode()
        # if message == "start game":
        #     self.fraction_choose_buttons_list = []
        # else:
        #     pass
        # game_started = self.sock.recv(1024).decode()
        # if game_started == "started":
        #     self.fraction_choose_buttons_list = []
        # else:
        #     pass
