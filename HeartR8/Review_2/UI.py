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
    def __init__(self, text, start_y, start_x, font=18, color=arcade.color.BRONZE):
        self.start_y = start_y
        self.start_x = start_x
        self.text = text
        self.font = font
        self.color = color

    def draw_text(self):
        arcade.draw_text(self.text, self.start_x, self.start_y,
                        self.color, self.font,
                        width=400, align="center", bold=True,
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
    def __init__(self, center_x, center_y, action_function, text, size_x=180, size_y=40):
        super().__init__(center_x, center_y, size_x, size_y, text, 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class CreateUnitButton(TextButton):
    def __init__(self, center_x, center_y, size_x, size_y, action_function, unit_type, text, cell_size, base_position):
        super().__init__(center_x, center_y, size_x, size_y, text, 18, "Arial")
        self.action_function = action_function
        self.unit_type = unit_type
        self.cell_size = cell_size
        self.base_position = base_position

    def on_press(self):
        super().on_press()
        self.action_function(self.unit_type, self.cell_size, self.base_position)


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


class FractionChooseButton(TextButton):
    def __init__(self, center_x, center_y, action_function, fraction, text):
        super().__init__(center_x, center_y, 140, 40, text, 18, "Arial")
        self.action_function = action_function
        self.fraction = fraction

    def on_release(self):
        super().on_release()
        self.action_function(self.fraction)
