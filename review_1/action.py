# deals with the physical aspect of actions

import UI
from mapping import raw_to_cell, cell_to_raw
from arcade import Sprite
from tech_bits import Singleton


# a singleton that gets sent whenever some action violates game logic
# it is immediately destroyed by main.MyGame's update method
class Dummy(Sprite, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        pass

    def update(self):
        self.kill()


# the base class for bolt-like actions
class BaseBolt(Sprite):
    def __init__(self, start_cell, end_cell, angle, rotation, speed_factor_x, speed_factor_y, sprite_pic, sprite_scale):
        super().__init__(sprite_pic, sprite_scale)
        a = end_cell.x - start_cell.x
        b = end_cell.y - start_cell.y
        hyp = (a ** 2 + b ** 2) ** 0.5
        a /= hyp
        b /= hyp
        self.end_cell = end_cell
        x, y = cell_to_raw(start_cell)
        self.center_x = x + UI.ACTION_DELTA * a
        self.center_y = y + UI.ACTION_DELTA * b
        self.change_x = UI.BOLT_SPEED * a
        self.change_y = UI.BOLT_SPEED * b
        self.angle = angle
        self.rotation = rotation
        self.speed_factor_x = speed_factor_x
        self.speed_factor_y = speed_factor_y

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.rotation
        if self.center_x < 0 or self.center_y < 0 or self.center_x > UI.SCREEN_WIDTH or self.center_y > UI.SCREEN_HEIGHT:
            self.kill()
        if self.end_cell == self.current_cell():
            self.kill()
        self.change_x *= self.speed_factor_x
        self.change_y *= self.speed_factor_y

    def current_cell(self):
        return raw_to_cell(self.center_x, self.center_y)
