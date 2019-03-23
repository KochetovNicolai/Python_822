import arcade
import UI


class Unit(arcade.Sprite):
    def __init__(self, center_x, center_y, sprite_pic, name):
        super().__init__(sprite_pic, UI.SPRITE_SCALING_UNIT)
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = 0
        self.change_y = 0
        self.turn_posx = center_x
        self.turn_posy = center_y
        self.name = name
        self.hp = 300

    def super(self):
        return super()

    def update(self):
        def stay_inside_window():
            if self.center_x < 0:
                self.center_x = 0
            if self.center_y < 0:
                self.center_y = 0
            if self.center_x > UI.SCREEN_WIDTH:
                self.center_x = UI.SCREEN_WIDTH
            if self.center_y > UI.SCREEN_HEIGHT:
                self.center_y = UI.SCREEN_HEIGHT

        def stay_inside_move_circle():
            x = self.turn_posx - self.center_x
            y = self.turn_posy - self.center_y
            if x ** 2 + y ** 2 > UI.RADIUS_OF_MOVEMENT ** 2:  # можно подправить логику
                self.center_x -= self.change_x
                self.center_y -= self.change_y

        self.center_x += self.change_x
        self.center_y += self.change_y
        stay_inside_window()
        stay_inside_move_circle()

    def draw(self):  # используется в on_draw in main.py
        arcade.draw_circle_outline(self.turn_posx, self.turn_posy, UI.RADIUS_OF_MOVEMENT, arcade.color.BLUE_YONDER,
                                   border_width=5)
        arcade.draw_text(f"{self.name}\nhp : {self.hp}", self.turn_posx - UI.RADIUS_OF_MOVEMENT + 30,
                         self.turn_posy - UI.RADIUS_OF_MOVEMENT + 50, arcade.color.WHITE, 20)

    def make_move(self, key):
        if key == arcade.key.RIGHT:
            self.change_x = UI.UNIT_SPEED
        if key == arcade.key.DOWN:
            self.change_y = -UI.UNIT_SPEED
        if key == arcade.key.LEFT:
            self.change_x = -UI.UNIT_SPEED
        if key == arcade.key.UP:
            self.change_y = UI.UNIT_SPEED

    def stop_move(self, key):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.change_x = 0
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.change_y = 0

    def turn_pos_update(self, x, y):
        self.turn_posx = x
        self.turn_posy = y
