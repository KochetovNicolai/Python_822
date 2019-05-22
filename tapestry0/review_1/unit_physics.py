# deals with the physical aspect of units

from arcade import Sprite, color, text
import config
from mapping import cell_to_raw, highlight


# the base class for units
class UnitPhysics(Sprite):
    def __init__(self, unit):  # should supply cell as an argument in the end
        super().__init__(unit.pic, config.SPRITE_SCALING_UNIT)
        self.unit = unit
        self.center_x, self.center_y = cell_to_raw(unit.cell)

    def update(self):
        if not self.unit.is_alive():
            self.kill()
        self.center_x, self.center_y = cell_to_raw(self.unit.cell)

    def draw(self):
        highlight(self.unit.cell, _color=color.WHITE)
        x, y = self.center_x - config.CELL_SIZE / 2, self.center_y - config.CELL_SIZE / 2
        text.draw_text(f"{self.unit.name}", x, y, color.GOLD, 30)

    def __repr__(self):
        return self.unit.name

    def get_object(self):
        return self.unit
