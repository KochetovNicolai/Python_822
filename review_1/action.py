import arcade
import UI


class Bolt(arcade.Sprite):
    def __init__(self, center_x, center_y, change_x, change_y, sprite_pic):
        super().__init__(sprite_pic, UI.SPRITE_SCALING_ACTION)
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = 100
        self.damage = 150

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += 10
        if self.center_x < 0 or self.center_y < 0 or self.center_x > UI.SCREEN_WIDTH or self.center_y > UI.SCREEN_HEIGHT:
            self.kill()
        self.change_x *= 0.99
        self.change_y *= 0.99
        self.damage *= 0.98
