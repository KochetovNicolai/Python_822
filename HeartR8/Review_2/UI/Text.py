import arcade


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
