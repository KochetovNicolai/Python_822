import arcade


def check_mouse_press_for_buttons(x, y, button_list):
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(x, y, button_list):
    for button in button_list:
        if button.pressed:
            button.on_release()


class Text:
    def __init__(self, text, start_y, start_x):
        self.start_y = start_y
        self.start_x = start_x
        self.text = text

    def draw_text(self):
        arcade.draw_text(self.text, self.start_x, self.start_y,
                        arcade.color.BLACK, 14,
                        width=400, align="center",
                        anchor_x="center", anchor_y="center")


class TextButton:
    def __init__(self,
                 center_x,
                 center_y,
                 width,
                 height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)
        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


class StartTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function, text):
        super().__init__(center_x, center_y, 100, 40, text, 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class CreateUnitButton(TextButton):
    def __init__(self, center_x, center_y, action_function, unit_type,  text, cell_size):
        super().__init__(center_x, center_y, 150, 40, text, 18, "Arial")
        self.action_function = action_function
        self.unit_type = unit_type
        self.cell_size = cell_size

    def on_release(self):
        super().on_release()
        self.action_function(self.unit_type, self.cell_size)


class UnitButton(TextButton):
    def __init__(self, center_x, center_y, action_function, text, nickname, cell_size):
        super().__init__(center_x, center_y, 40, 40, text, 8, "Arial", face_color=arcade.color.LAPIS_LAZULI)
        self.action_function = action_function
        self.player_nickname = nickname
        self.player_now = ''
        self.center_x = center_x
        self.center_y = center_y
        self.cell_size = cell_size

    def on_press(self):
        if self.player_nickname == self.player_now:
            if not self.pressed:
                self.action_function(self.center_x, self.center_y, self.cell_size, self.player_nickname)
                self.pressed = True
            else:
                self.pressed = False

    def on_release(self):
        pass


class HighlightedCellButton(TextButton):
    def __init__(self, center_x, center_y, action_function, text, nickname):
        super().__init__(center_x, center_y, 40, 40, text, 8, "Arial", face_color=arcade.color.YELLOW)
        self.action_function = action_function
        self.player_nickname = nickname
        self.player_now = ''

    def on_press(self):
        if self.player_nickname == self.player_now:
            if not self.pressed:
                self.action_function()
                self.pressed = True
            else:
                self.pressed = False

    def on_release(self):
        pass
