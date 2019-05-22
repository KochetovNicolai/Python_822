from action_manager import create_attack_action
from config import UNIT_PIC
from tech_bits import Dummy
from mapping import cab_distance, get_cell


# main unit properties
class Stats:
    def __init__(self, hp, speed, damage, items, vision, actions):
        self.hp = hp
        self.hp_limit = hp
        self.speed = speed
        self.damage = damage
        self.items = items
        self.vision = vision
        self.actions = actions

    def set(self, *, hp=None, speed=None, damage=None, items=None, vision=None, actions=None):
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


class Unit:
    def __init__(self, cell, name, pic, stats):
        self.cell = cell
        self.name = name
        self.pic = pic

        self.stats = stats
        self.physics = None
        self.states = None
        self.activity = None

    def kill(self):
        self.stats.hp = 0
        self.cell.reset()

    def update(self):
        if self.stats.hp < 0:
            self.stats.hp = 0
        if self.stats.hp > self.stats.hp_limit:
            self.stats.hp = self.stats.hp_limit

    def is_alive(self):
        return self.stats.hp > 0

    def attack(self, cell):  # to be overloaded in later releases
        pass

    def skill(self):  # to be overloaded in later releases
        pass

    def display(self):
        self.stats.display()


class Fighter(Unit):
    item_id = 1
    items = [item_id]
    FighterStats = {"hp": 200, "speed": 6, "damage": 70, "items": items, "vision": 7, "actions": 3}

    def __init__(self, cell, name):
        super().__init__(cell, name, UNIT_PIC, Stats(**Fighter.FighterStats))

    def __repr__(self):
        return "Fighter"

    def attack(self, cell):
        if cab_distance(get_cell(self), cell) > 1:
            return create_attack_action("handaxe", self, cell,
                                        damage=self.stats.damage, damage_factor=1)
        else:
            return Dummy()


class Mage(Unit):
    item_id = 2
    items = [item_id]
    MageStats = {"hp": 50, "speed": 10, "damage": 40, "items": items, "vision": 8, "actions": 4}

    def __init__(self, cell, name):
        super().__init__(cell, name, UNIT_PIC, Stats(**Mage.MageStats))

    def __repr__(self):
        return "Mage"

    def attack(self, cell):
        if cab_distance(get_cell(self), cell) > 1:
            return create_attack_action("fireball", self, cell,
                                        damage=self.stats.damage, damage_factor=0.98)
        else:
            return Dummy()


class Craftsman(Unit):
    item_id = 3
    items = [item_id]
    CraftsmanStats =\
        {"hp": 150, "speed": 12, "damage": 10, "items": items, "vision": 10, "actions": 5}

    def __init__(self, cell, name):
        super().__init__(cell, name, UNIT_PIC, Stats(**Craftsman.CraftsmanStats))

    def __repr__(self):
        return "Craftsman"

    def attack(self, cell):
        if cab_distance(get_cell(self), cell) > 1:
            return create_attack_action("pickaxe", self, cell,
                                        damage=self.stats.damage, damage_factor=0.8)
        else:
            return Dummy()


class Ranger(Unit):
    item_id = 4
    items = [item_id]
    RangerStats = {"hp": 100, "speed": 8, "damage": 30, "items": items, "vision": 9, "actions": 4}

    def __init__(self, cell, name):
        super().__init__(cell, name, UNIT_PIC, Stats(**Ranger.RangerStats))

    def __repr__(self):
        return "Ranger"

    def attack(self, cell):
        if cab_distance(get_cell(self), cell) > 1:
            return create_attack_action("arrow", self, cell,
                                        damage=self.stats.damage, damage_factor=0.95)
        else:
            return Dummy()
