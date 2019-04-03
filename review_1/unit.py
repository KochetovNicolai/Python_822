# deals with the physical aspect of units

from arcade import Sprite, draw_text, color
import UI
from mapping import cell_to_raw


# the base class for units
class BaseUnit(Sprite):
    def __init__(self, cell, name, pic):  # should supply cell as an argument in the end
        super().__init__(pic, UI.SPRITE_SCALING_UNIT)
        self.cell = cell
        self.center_x, self.center_y = cell_to_raw(cell)
        self.name = name

    def update(self):
        self.center_x, self.center_y = cell_to_raw(self.cell)

    def __repr__(self):
        return self.name
