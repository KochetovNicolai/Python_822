# establishes in-game unit types and their main properties

from unit import BaseUnit
from arcade import draw_commands, text, color
import UI
from action_manager import create_action
from action import Dummy
from mapping import cab_distance, get_cell


# main unit properties
class Stats:
    def __init__(self, hp, speed, damage, items, vision, actions=3):
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.items = items
        self.vision = vision
        self.actions = actions

    def set(self, hp=None, speed=None, damage=None, items=None, vision=None, actions=None):
        if hp is not None:
            self.hp = hp
        if speed is not None:
            self.speed = speed
        if damage is not None:
            self.damage = damage
        if items is not None:
            self.items = items
        if vision is not None:
            self.vision = vision
        if actions is not None:
            self.actions = actions

    # displays properties in the right upper corner of the screen when the mouse cursor hovers over self
    def display(self):
        if self.hp > 0:
            draw_commands.draw_lrtb_rectangle_filled(left=UI.SCREEN_WIDTH - 130, right=UI.SCREEN_WIDTH,
                                                     top=UI.SCREEN_HEIGHT, bottom=UI.SCREEN_HEIGHT - 100,
                                                     color=(1, 1, 1))
            output = f"hp: {self.hp}\nspeed: {self.speed}\ndamage: {self.damage}\nitems: {self.items}\nvision: {self.vision}"
            text.draw_text(text=output, start_x=UI.SCREEN_WIDTH - 130 + 10, start_y=UI.SCREEN_HEIGHT - 100,
                           color=color.WHITE,
                           font_size=18)


UNIT_PIC = "sprite_pictures/head.png"  # for now by default


class Unit(BaseUnit):
    def __init__(self, cell, name, pic, stats):
        super().__init__(cell, name, pic)
        self.stats = stats

    def update(self):
        super().update()
        if self.stats.hp < 0:
            self.stats.hp = 0

    # displays's unit's name
    def draw(self):
        x, y = self.center_x, self.center_y
        text.draw_text(f"{self.name}", x - UI.CELL_SIZE + 30,
                       y - UI.CELL_SIZE + 50, color.BLUE_YONDER, 20)

    def is_alive(self):
        return self.stats.hp > 0

    def attack(self, cell):  # to be overloaded in later releases
        pass

    def skill(self):  # to be overloaded in later releases
        pass

    def display(self):
        self.stats.display()


# item_id and items are placeholders
# cab_distance checks in attack methods are a temporary solution for the problem 1 detailed in main.py
# Dummy is described in action.py

class Fighter(Unit):
    item_id = 1
    items = [item_id]
    stats = {"hp": 200, "speed": 6, "damage": 70, "items": items, "vision": 7}

    def __init__(self, cell, name):
        super().__init__(cell, name, UNIT_PIC, Stats(**Fighter.stats))

    def attack(self, cell):
        if cab_distance(get_cell(self), cell) > 1:
            return create_action("handaxe", self, cell, damage=self.stats.damage, damage_factor=1)
        else:
            return Dummy()


class Mage(Unit):
    item_id = 2
    items = [item_id]
    stats = {"hp": 50, "speed": 10, "damage": 40, "items": items, "vision": 8}

    def __init__(self, cell, name):
        super().__init__(cell, name, UNIT_PIC, Stats(**Mage.stats))

    def attack(self, cell):
        if cab_distance(get_cell(self), cell) > 1:
            return create_action("fireball", self, cell, damage=self.stats.damage, damage_factor=0.98)
        else:
            return Dummy()


class Craftsman(Unit):
    item_id = 3
    items = [item_id]
    stats = {"hp": 150, "speed": 12, "damage": 10, "items": items, "vision": 10}

    def __init__(self, cell, name):
        super().__init__(cell, name, UNIT_PIC, Stats(**Craftsman.stats))

    def attack(self, cell):
        if cab_distance(get_cell(self), cell) > 1:
            return create_action("pickaxe", self, cell, damage=self.stats.damage, damage_factor=0.8)
        else:
            return Dummy()


class Ranger(Unit):
    item_id = 4
    items = [item_id]
    stats = {"hp": 100, "speed": 8, "damage": 30, "items": items, "vision": 9}

    def __init__(self, cell, name):
        super().__init__(cell, name, UNIT_PIC, Stats(**Ranger.stats))

    def attack(self, cell):
        if cab_distance(get_cell(self), cell) > 1:
            return create_action("arrow", self, cell, damage=self.stats.damage, damage_factor=0.95)
        else:
            return Dummy()
