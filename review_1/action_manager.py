# a module for managing actions

from action import BaseBolt
import UI
from mapping import angle, get_cell, is_rocky, is_water


# meaningful game properties for attaching to action.py's basic physical models
class Modifiers:
    def __init__(self, damage=0, damage_factor=1, heal=0, heal_factor=1):
        self.damage = damage
        self.damage_factor = damage_factor
        self.heal = heal
        self.heal_factor = heal_factor

    def set(self, *, damage=None, damage_factor=None, heal=None, heal_factor=None):
        if damage is not None:
            self.damage = damage
        if damage_factor is not None:
            self.damage_factor = damage_factor
        if heal is not None:
            self.heal = heal
        if heal_factor is not None:
            self.heal_factor = heal_factor


class Bolt(BaseBolt):
    def __init__(self, creator, destination, **parameters):
        super().__init__(get_cell(creator), destination, **parameters)
        self.modifiers = Modifiers()

    def update(self):
        super().update()
        self.modifiers.damage *= self.modifiers.damage_factor
        if abs(self.change_x) < UI.BOLT_SPEED_LIMIT and abs(self.change_y) < UI.BOLT_SPEED_LIMIT:
            # destroys action's sprite if it slows down too much (otherwise it would freeze on the map)
            self.kill()
        if is_rocky(self.current_cell()):  # no bolt penetrates mountains
            self.kill()


class Fireball(Bolt):
    parameters = {"angle": 0,
                  "rotation": 10,
                  "speed_factor_x": 0.98,
                  "speed_factor_y": 0.98,
                  "sprite_pic": "sprite_pictures/fireball.png",
                  "sprite_scale": 0.05}

    def __init__(self, creator, destination):
        super().__init__(creator, destination, **Fireball.parameters)

    def update(self):
        super().update()
        if is_water(self.current_cell()):  # fireball is extinguished on water terrain
            self.kill()


class Arrow(Bolt):
    parameters = {"rotation": 0,
                  "speed_factor_x": 0.99,
                  "speed_factor_y": 0.99,
                  "sprite_pic": "sprite_pictures/arrow.png",
                  "sprite_scale": 0.12}

    def __init__(self, creator, destination):
        angle_ = 135 + angle(get_cell(creator), destination)
        super().__init__(creator, destination, angle=angle_, **Arrow.parameters)


class Pickaxe(Bolt):
    parameters = {"rotation": 0,
                  "speed_factor_x": 0.99,
                  "speed_factor_y": 0.99,
                  "sprite_pic": "sprite_pictures/pickaxe.png",
                  "sprite_scale": 0.3}

    def __init__(self, creator, destination):
        angle_ = -50 + angle(get_cell(creator), destination)
        super().__init__(creator, destination, angle=angle_, **Pickaxe.parameters)


class Handaxe(Bolt):
    parameters = {"angle": 0,
                  "rotation": 5,
                  "speed_factor_x": 0.98,
                  "speed_factor_y": 0.98,
                  "sprite_pic": "sprite_pictures/handaxe.png",
                  "sprite_scale": 0.18}

    def __init__(self, creator, destination):
        super().__init__(creator, destination, **Handaxe.parameters)


def create_action(action_name, origin, destination, damage=None, damage_factor=None):
    action = None
    if action_name == "fireball":
        action = Fireball(origin, destination)
    elif action_name == "arrow":
        action = Arrow(origin, destination)
    elif action_name == "pickaxe":
        action = Pickaxe(origin, destination)
    elif action_name == "handaxe":
        action = Handaxe(origin, destination)
    action.modifiers.set(damage=damage, damage_factor=damage_factor)
    return action
