import arcade
from UI.Buttons.TextButton import TextButton


class UnitButton(TextButton):
    def __init__(self, x, y, center_x, center_y, action_function, action_function_on_release, text, nickname, cell_size):
        super().__init__(center_x, center_y, 40, 40, text, 8, "Arial", face_color=arcade.color.LAPIS_LAZULI)
        self.action_function = action_function
        self.action_function_on_release = action_function_on_release
        self.player_nickname = nickname
        self.player_now = ''
        self.x = x
        self.y = y
        self.center_x = center_x
        self.center_y = center_y
        self.cell_size = cell_size

    def on_press(self):
        if not self.pressed:
            self.action_function(self.x, self. y, self.cell_size, self.player_nickname)
            self.pressed = True
        else:
            self.pressed = False
            self.action_function_on_release()

    def on_release(self):
        pass
