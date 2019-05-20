import arcade
import random
from Multiplayer import multiplayer_field, multiplayer_classes
from threading import Thread
import os
import pickle


class MyGame(arcade.Window):
    def __init__(self, field_size, player_list, name_list, server_players_list):
        print(os.getcwd())
        self.player_number = len(server_players_list)
        self.server_players_list = server_players_list
        self.name_list = name_list
        self.button_list = None
        self.player_list = player_list
        self.field = multiplayer_field.GameField(field_size)
        self.turn = 0
        self.unit_list = []
        self.highlighted_cells = []
        self.game_started = False
        self.background = None
        self.fractions_chosen = False
        self.frac_list = [multiplayer_classes.CriminalFraction,
                          multiplayer_classes.MajorsFraction,
                          multiplayer_classes.PartyFraction,
                          multiplayer_classes.BotansFraction]
        self.fraction_choose_buttons_list = []
        self.fraction_names = ['Преступники',
                               'Мажоры',
                               'Тусовщики',
                               'Ботаны']
        self.add_money = 20
        self.units_amount = 4
        self.game_continues = True

    def setup(self):
        self.divide_players_into_threads()
        self.button_list = []

    def update(self, delta_time):
        pass
        # if self.game_started:
        #
        #     self.unit_list = []
        #     self.highlighted_cells = []
        #     self.field.field_info = [[None for i in range(self.field.size)] for j in range(self.field.size)]
        #
        #     for i in self.player_list:
        #
        #         if i.next_turn and (i.money == 0):
        #             i.next_turn = False
        #             self.next_player()
        #
        #         for j in i.button_list:
        #             j.player_now = self.player_list[self.turn].name
        #             self.unit_list.append(j)
        #
        #         for j in i.highlighted_cells_list:
        #             j.player_now = self.player_list[self.turn].name
        #             self.highlighted_cells.append(j)
        #
        #         for j in range(0, len(i.unit_list)):
        #             self.field.field_info[i.unit_list[j].unit_place[0] - 1][i.unit_list[j].unit_place[1] - 1] = \
        #                 [i.name, 'Unit', j]
        #
        #         self.field.field_info[i.base.place[0] - 1][i.base.place[1] - 1] = [i.name, 'Base']
        #
        #         i.player_list = self.player_list
        #         i.field_info = self.field.field_info[:]

    def send_fractions_chosen_message(self):
        for player in self.server_players_list:
            player.send(bytes("start game", "UTF-8"))

    def start_session(self, player):
        while not self.game_started:
            message = player.recv(1024).decode()
            if not self.game_started:
                self.create_fraction(message, player)
            else:
                break
            print(self.player_list)
            print('Игрок {} выбрал {}'.format(self.server_players_list.index(player) + 1, message))
            print(self.game_started)

    def send_field_size(self, player):
        player.send(bytes(str(self.field.size), "UTF-8"))
        print("sent field size to player {}".format(self.name_list[self.server_players_list.index(player)]))
        print()

    def send_number_of_players(self, player):
        player.send(bytes(str(self.player_number), "UTF-8"))
        print("sent number of players to player {}".format(self.name_list[self.server_players_list.index(player)]))
        print()

    def send_place_of_bases(self, player):
        bases_dict = {}
        for pl in self.player_list:
            bases_dict[pl.name] = pl.base.place
        player.send(pickle.dumps(bases_dict))

    def run_command(self, message, player):
        message = message
        if message == "get field size":
            self.send_field_size(player)
        if message == "number of players":
            self.send_number_of_players(player)
        if message == "place of bases":
            self.send_place_of_bases(player)
        if message.startswith("create unit"):
            self.player_list[self.server_players_list.index(player)].create_unit(message)

    def check_for_messages(self, player):
        while self.game_continues:
            player.setblocking(0)
            player.settimeout(0.1)
            message = ""
            try:
                message = player.recv(1024).decode()
                print("checked player {}".format(self.name_list[self.server_players_list.index(player)]))
                print('received message "{}" from player {}'.format(message, self.name_list[self.server_players_list.index(player)]))
            except:
                pass
            if message != "":
                self.run_command(message, player)
            player.setblocking(1)

    def player_thread(self, player):
        player.send(bytes("start", "UTF-8"))
        self.start_session(player)
        self.check_for_messages(player)

    def divide_players_into_threads(self):
        threads = []  # список всех работающих потоков

        for player in self.server_players_list:  # делим работу на потоки
            thr = Thread(target=self.player_thread, args=(player, ))
            threads.append(thr)
            thr.start()

        for thr in threads:  # ждем завершения всех потоков
            thr.join()

    # def start_game_program(self):
    #     self.game_started = True
    #     self.button_list.remove(self.button_list[3])
    #     self.button_list.remove(self.button_list[2])

    # def close_program(self):
    #     self.close()

    def place_bases(self, i):
        self.player_list[i].base.place = [random.randint(1, self.field.size), random.randint(1, self.field.size)]
        self.field.base_list.append(self.player_list[i].base.place)

    # def refresh_program(self):
    #     self.field.base_list = []
    #     for i in range(len(self.player_list)):
    #         self.place_bases(i)

    def create_fraction(self, fraction, player):
        pl_num = self.server_players_list.index(player)
        self.player_list[pl_num] = \
            self.frac_list[self.fraction_names.index(fraction)](self.field.size)
        self.player_list[pl_num].name = self.name_list[pl_num]
        self.place_bases(pl_num)
        check = True
        for i in self.player_list:
            if i is None:
                check = False
        self.game_started = check
        if self.game_started:
            self.send_fractions_chosen_message()

    # def next_player(self):
    #     if self.turn < len(self.player_list):
    #         for i in self.player_list[self.turn].unit_list:
    #             i.participated_in_turn = True
    #     self.turn += 1
    #     if self.turn >= len(self.player_list):
    #         self.turn = 0
    #         self.fractions_chosen = True
    #         self.fraction_choose_buttons_list = []
    #     if self.game_started:
    #         self.player_list[self.turn].money += self.add_money
    #         self.player_list[self.turn].units_behave_list = []
    #         for i in self.player_list[self.turn].unit_list:
    #             self.player_list[self.turn].units_behave_list.append(i)
    #             i.participated_in_turn = False
    #         for i in self.player_list:
    #             i.highlighted_cells_list = []
    #             for j in i.button_list:
    #                 if j.pressed:
    #                     j.pressed = False
