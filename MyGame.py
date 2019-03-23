import arcade
import random
import UI
import GameField
import Game_classes


class MyGame(arcade.Window):
    def __init__(self, width, height, field_size, player_list):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.pause = False
        self.button_list = None
        self.player_list = player_list
        self.field = GameField.GameField(min(width, height) // 4 * 3, field_size)
        self.turn = 0
        self.place_bases()
        self.unit_list = []
        self.highlighted_cells_list = []

    def setup(self):
        self.button_list = []

        play_button = UI.StartTextButton(60, 30, self.resume_program, "Refresh")
        self.button_list.append(play_button)

        quit_button = UI.StartTextButton(200, 30, self.pause_program, "End")
        self.button_list.append(quit_button)

        next_button = UI.StartTextButton(340, 30, self.next_player, "Next Turn")
        self.button_list.append(next_button)

        create_unit_1_button = UI.CreateUnitButton(1000, 300, self.player_list[self.turn].create_unit,
                                                   Game_classes.Bydlan, '', self.field.cell_size)
        self.button_list.append(create_unit_1_button)

        create_unit_2_button = UI.CreateUnitButton(1000, 350, self.player_list[self.turn].create_unit,
                                                   Game_classes.Bariga, '', self.field.cell_size)
        self.button_list.append(create_unit_2_button)

        create_unit_3_button = UI.CreateUnitButton(1000, 400, self.player_list[self.turn].create_unit,
                                                   Game_classes.Offnik, '', self.field.cell_size)
        self.button_list.append(create_unit_3_button)

        create_unit_4_button = UI.CreateUnitButton(1000, 450, self.player_list[self.turn].create_unit,
                                                   Game_classes.Zek, '', self.field.cell_size)
        self.button_list.append(create_unit_4_button)

    def on_draw(self):
        arcade.start_render()
        self.field.draw_field()
        for button in self.button_list:
            button.draw()

        for button in self.unit_list:
            button.draw()

        for button in self.highlighted_cells_list:
            button.draw()

        for i in range(3, 7):
            self.button_list[i].action_function = self.player_list[self.turn].create_unit
            temporary = self.player_list[self.turn].name_units[i - 3]
            self.button_list[i].unit_type = temporary
            self.button_list[i].text = temporary.__name__

        for i in self.player_list:
            arcade.draw_rectangle_filled(i.base.place[0] * self.field.cell_size + 10 - self.field.cell_size // 2,
                                         i.base.place[1] * self.field.cell_size + 100 - self.field.cell_size // 2,
                                         self.field.cell_size - 5,
                                         self.field.cell_size - 5,
                                         color=arcade.color.RED)

        information_txt = UI.Text(self.player_list[self.turn].info_about_units(), 550, 700)
        information_txt.draw_text()

    def update(self, delta_time):
        self.unit_list = []
        for i in self.player_list:
            for j in i.button_list:
                j.player_now = self.player_list[self.turn].name
                self.unit_list.append(j)
        self.highlighted_cells_list = []
        for i in self.player_list:
            for j in i.highlighted_cells_list:
                j.player_now = self.player_list[self.turn].name
                self.highlighted_cells_list.append(j)

    def on_mouse_press(self, x, y, button, key_modifiers):
        UI.check_mouse_press_for_buttons(x, y, self.button_list)
        UI.check_mouse_press_for_buttons(x, y, self.unit_list)
        UI.check_mouse_press_for_buttons(x, y, self.highlighted_cells_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        UI.check_mouse_release_for_buttons(x, y, self.button_list)
        UI.check_mouse_release_for_buttons(x, y, self.unit_list)
        UI.check_mouse_release_for_buttons(x, y, self.highlighted_cells_list)

    def pause_program(self):
        self.pause = True

    def place_bases(self):
        for i in self.player_list:
            i.base.place = [random.randint(1, self.field.size), random.randint(1, self.field.size)]
            self.field.base_list.append(i.base.place)

    def resume_program(self):
        self.pause = False
        self.field.base_list = []
        self.place_bases()
        self.field.print_field_info()

    def next_player(self):
        self.turn += 1
        if self.turn >= len(self.player_list):
            self.turn = 0
