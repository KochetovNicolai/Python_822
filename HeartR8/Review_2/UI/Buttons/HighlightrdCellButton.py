import arcade
from UI.Buttons.TextButton import TextButton


class HighlightedCellButton(TextButton):
    def __init__(self, center_x, center_y, action_function, text, nickname,
                 x, y, unit_x, unit_y, cell_size, but_type):
        super().__init__(center_x, center_y, 40, 40, text, 8, "Arial")

        if but_type == 'move':
            self.face_color = arcade.color.YELLOW
        elif but_type == 'attack':
            self.face_color = arcade.color.RED
        elif but_type == 'attack_base':
            self.face_color = arcade.color.BLUE

        self.but_type = but_type
        self.action_function = action_function
        self.player_nickname = nickname
        self.player_now = ''
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.unit_x = unit_x
        self.unit_y = unit_y
        self.center_x = center_x
        self.center_y = center_y

    def on_release(self):
        if self.player_nickname == self.player_now:
            super().on_release()
            if self.but_type == 'move':
                self.action_function(self.x, self.y, self.unit_x, self.unit_y, self.player_nickname, self.cell_size)
            elif self.but_type == 'attack':
                self.action_function(self.x, self.y, self.unit_x, self.unit_y)
            elif self.but_type == 'attack_base':
                self.action_function(self.x, self.y, self.unit_x, self.unit_y)
