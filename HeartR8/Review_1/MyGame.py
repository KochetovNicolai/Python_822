import arcade
import random
import UI
import GameField
import Game_classes
import pygame


class MyGame(arcade.Window):
    def __init__(self, width, height, field_size, player_list, name_list):
        pygame.mixer.init()
        pygame.mixer.music.load('Background_music.wav')
        pygame.mixer.music.play(-1)
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.name_list = name_list
        self.width = width
        self.height = height
        self.pause = False
        self.button_list = None
        self.player_list = player_list
        self.field = GameField.GameField(min(width, height) // 4 * 3, field_size)
        self.turn = 0
        self.unit_list = []
        self.highlighted_cells = []
        self.game_started = False
        self.background = None
        self.fractions_chosen = False
        self.frac_list = [Game_classes.CriminalFraction,
                          Game_classes.MajorsFraction,
                          Game_classes.PartyFraction,
                          Game_classes.BotansFraction]
        self.fraction_choose_buttons_list = []
        self.fraction_names = ['Преступники',
                               'Мажоры',
                               'Тусовщики',
                               'Ботаны',]

    def setup(self):
        self.button_list = []
        self.background = arcade.load_texture("BG2.jpg")

        quit_button = UI.StartTextButton(100, 30, self.close_program, "Выход")
        self.button_list.append(quit_button)

        next_button = UI.StartTextButton(300, 30, self.next_player, "Следующий игрок")
        self.button_list.append(next_button)

        play_button = UI.StartTextButton(500, 30, self.refresh_program, "Обновить")
        self.button_list.append(play_button)

        start_game_button = UI.StartTextButton(700, 30, self.start_game_program, "Старт")
        self.button_list.append(start_game_button)

        self.player_list[0] = self.frac_list[0](self.field.size)

        create_unit_1_button = UI.CreateUnitButton(1000, 450, self.player_list[0].create_unit,
                                                   Game_classes.Zek, '', self.field.cell_size, self.player_list[0].base.place)
        self.button_list.append(create_unit_1_button)

        create_unit_2_button = UI.CreateUnitButton(1000, 400, self.player_list[0].create_unit,
                                                   Game_classes.Bariga, '', self.field.cell_size, self.player_list[0].base.place)
        self.button_list.append(create_unit_2_button)

        create_unit_3_button = UI.CreateUnitButton(1000, 350, self.player_list[0].create_unit,
                                                   Game_classes.Offnik, '', self.field.cell_size, self.player_list[0].base.place)
        self.button_list.append(create_unit_3_button)

        create_unit_4_button = UI.CreateUnitButton(1000, 300, self.player_list[0].create_unit,
                                                   Game_classes.Bydlan, '', self.field.cell_size, self.player_list[0].base.place)
        self.button_list.append(create_unit_4_button)

        for i in range(len(self.frac_list)):
            self.fraction_choose_buttons_list.append(UI.FractionChooseButton(self.width // 2,
                                                                             self.height // 2 - 100 + 50 * i,
                                                                             self.create_fraction,
                                                                             self.frac_list[i],
                                                                             self.fraction_names[i]))

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.width, self.height, self.background)

        if self.fractions_chosen:
            self.field.draw_field()

            if self.game_started:
                for button in self.button_list:
                    button.draw()
            else:
                for button in range(len(self.button_list) - 4):
                    self.button_list[button].draw()

            for button in self.unit_list:
                button.draw()

            for button in self.highlighted_cells:
                button.draw()

            if self.game_started:
                for i in range(len(self.button_list) - 4, len(self.button_list)):
                    self.button_list[i].action_function = self.player_list[self.turn].create_unit
                    temporary = self.player_list[self.turn].name_units[i - len(self.button_list) + 4]
                    self.button_list[i].unit_type = temporary
                    temporary = self.player_list[self.turn].name_units_text[i - len(self.button_list) + 4]
                    self.button_list[i].text = temporary
                    temporary = self.player_list[self.turn].base.place
                    self.button_list[i].base_position = temporary

            for i in self.player_list:
                arcade.draw_rectangle_filled(i.base.place[0] * self.field.cell_size + 10 - self.field.cell_size // 2,
                                             i.base.place[1] * self.field.cell_size + 100 - self.field.cell_size // 2,
                                             self.field.cell_size - 5,
                                             self.field.cell_size - 5,
                                             color=arcade.color.GRAY_ASPARAGUS)
                base_owner = UI.Text(i.name,
                                     i.base.place[1] * self.field.cell_size + 100 - self.field.cell_size // 2,
                                     i.base.place[0] * self.field.cell_size + 10 - self.field.cell_size // 2)
                base_owner.draw_text()

            information_txt = UI.Text(self.player_list[self.turn].info_about_units(), 450, 700,
                                      font=16)
            information_txt.draw_text()

            self.player_list[self.turn].unit_info.draw_text()
        else:
            for button in self.fraction_choose_buttons_list:
                button.draw()
                text = UI.Text('Игрок {}'.format(self.turn + 1), self.height // 2 + 150, self.width // 2)
                text.draw_text()

    def update(self, delta_time):
        if self.game_started:
            self.unit_list = []
            for i in self.player_list:
                for j in i.button_list:
                    j.player_now = self.player_list[self.turn].name
                    self.unit_list.append(j)
            self.highlighted_cells = []
            for i in self.player_list:
                for j in i.highlighted_cells_list:
                    j.player_now = self.player_list[self.turn].name
                    self.highlighted_cells.append(j)
            self.field.field_info = [[None for i in range(self.field.size)] for j in range(self.field.size)]
            for i in self.player_list:
                for j in range(0, len(i.unit_list)):
                    self.field.field_info[i.unit_list[j].unit_place[0] - 1][i.unit_list[j].unit_place[1] - 1] = \
                        [i.name, 'Unit', j]
            for i in self.player_list:
                self.field.field_info[i.base.place[0] - 1][i.base.place[1] - 1] = [i.name, 'Base']
            for i in self.player_list:
                i.player_list = self.player_list
                i.field_info = self.field.field_info[:]
            for i in self.player_list:
                if i.next_turn and (i.money == 0):
                    i.next_turn = False
                    self.next_player()

    def on_mouse_press(self, x, y, button, key_modifiers):
        UI.check_mouse_press_for_buttons(x, y, self.button_list)
        UI.check_mouse_press_for_buttons(x, y, self.unit_list)
        UI.check_mouse_press_for_buttons(x, y, self.highlighted_cells)
        UI.check_mouse_press_for_buttons(x, y, self.fraction_choose_buttons_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        UI.check_mouse_release_for_buttons(x, y, self.button_list)
        UI.check_mouse_release_for_buttons(x, y, self.unit_list)
        UI.check_mouse_release_for_buttons(x, y, self.highlighted_cells)
        UI.check_mouse_release_for_buttons(x, y, self.fraction_choose_buttons_list)

    def start_game_program(self):
        self.game_started = True
        self.button_list.remove(self.button_list[3])
        self.button_list.remove(self.button_list[2])

    def close_program(self):
        self.close()

    def place_bases(self, i):
        self.player_list[i].base.place = [random.randint(1, self.field.size), random.randint(1, self.field.size)]
        self.field.base_list.append(self.player_list[i].base.place)

    def refresh_program(self):
        self.pause = False
        self.field.base_list = []
        for i in range(len(self.player_list)):
            self.place_bases(i)

    def create_fraction(self, fraction):
        self.player_list[self.turn] = fraction(self.field.size)
        self.player_list[self.turn].name = self.name_list[self.turn]
        self.place_bases(self.turn)
        if self.turn == 0:
            self.player_list[self.turn].money = 2
        self.next_player()

    def next_player(self):
        for i in self.player_list[self.turn].unit_list:
            i.participated_in_turn = True
        self.turn += 1
        if self.turn >= len(self.player_list):
            self.turn = 0
            self.fractions_chosen = True
        if self.game_started:
            self.player_list[self.turn].money += 2
            self.player_list[self.turn].units_behave_list = []
            for i in self.player_list[self.turn].unit_list:
                self.player_list[self.turn].units_behave_list.append(i)
                i.participated_in_turn = False
            for i in self.player_list:
                i.highlighted_cells_list = []
                for j in i.button_list:
                    if j.pressed:
                        j.pressed = False
