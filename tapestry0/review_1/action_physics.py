import math
from arcade import Sprite
from mapping import raw_to_cell, cell_to_raw, get_cell, angle
import config


def outside_screen(x, y):
    return x < 0 or y < 0 \
           or x > config.SCREEN_WIDTH or y > config.SCREEN_HEIGHT


class ActionPhysics(Sprite):
    def __init__(self, action, sprite_pic, sprite_scale):
        super().__init__(sprite_pic, sprite_scale)
        self.action = action

    def update(self):
        if not self.action.exists():
            self.kill()

    def current_cell(self):
        return raw_to_cell(self.center_x, self.center_y)

    def get_object(self):
        return self.action


def vector(a, b):
    hyp = (a ** 2 + b ** 2) ** 0.5
    return a / hyp, b / hyp


class BoltPhysics(ActionPhysics):
    def __init__(self, bolt, start_cell, end_cell, angle, rotation,
                 speed_factor_x, speed_factor_y, sprite_pic, sprite_scale):
        super().__init__(bolt, sprite_pic, sprite_scale)

        a, b = vector(end_cell.x - start_cell.x,
                      end_cell.y - start_cell.y)
        self.end_cell = end_cell
        x, y = cell_to_raw(start_cell)
        self.center_x = x + config.ACTION_DELTA * a
        self.center_y = y + config.ACTION_DELTA * b
        self.change_x = config.BOLT_SPEED * a
        self.change_y = config.BOLT_SPEED * b
        self.angle = angle
        self.rotation = rotation
        self.speed_factor_x = speed_factor_x
        self.speed_factor_y = speed_factor_y

    def update(self):
        super().update()

        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.rotation
        if outside_screen(self.center_x, self.change_y):
            self.kill()
        if self.end_cell == self.current_cell():
            self.kill()
        self.change_x *= self.speed_factor_x
        self.change_y *= self.speed_factor_y

        if abs(self.change_x) < config.BOLT_SPEED_LIMIT \
                and abs(self.change_y) < config.BOLT_SPEED_LIMIT:
            self.kill()


class FireballPhysics(BoltPhysics):
    parameters = {"angle": 0,
                  "rotation": 10,
                  "speed_factor_x": 0.98,
                  "speed_factor_y": 0.98,
                  "sprite_pic": "sprite_pictures/fireball.png",
                  "sprite_scale": 0.05}

    def __init__(self, bolt, creator, destination):
        super().__init__(bolt, get_cell(creator), destination, **FireballPhysics.parameters)


class ArrowPhysics(BoltPhysics):
    parameters = {"rotation": 0,
                  "speed_factor_x": 0.99,
                  "speed_factor_y": 0.99,
                  "sprite_pic": "sprite_pictures/arrow.png",
                  "sprite_scale": 0.12}

    def __init__(self, bolt, creator, destination):
        angle_ = 135 + angle(get_cell(creator), destination)
        super().__init__(bolt, get_cell(creator), destination,
                         angle=angle_, **ArrowPhysics.parameters)


class PickaxePhysics(BoltPhysics):
    parameters = {"rotation": 0,
                  "speed_factor_x": 0.99,
                  "speed_factor_y": 0.99,
                  "sprite_pic": "sprite_pictures/pickaxe.png",
                  "sprite_scale": 0.3}

    def __init__(self, bolt, creator, destination):
        angle_ = -50 + angle(get_cell(creator), destination)
        super().__init__(bolt, get_cell(creator), destination,
                         angle=angle_, **PickaxePhysics.parameters)


class HandaxePhysics(BoltPhysics):
    parameters = {"angle": 0,
                  "rotation": 5,
                  "speed_factor_x": 0.98,
                  "speed_factor_y": 0.98,
                  "sprite_pic": "sprite_pictures/handaxe.png",
                  "sprite_scale": 0.13}

    def __init__(self, bolt, creator, destination):
        super().__init__(bolt, get_cell(creator), destination, **HandaxePhysics.parameters)


class AuraPhysics(ActionPhysics):
    def __init__(self, aura, radius, sprite_pic, sprite_scale):
        super().__init__(aura, sprite_pic, sprite_scale)

        self.radius = radius
        self.angle = math.pi / 2
        self.rotation = config.AURA_ROTATION_SPEED
        x, y = cell_to_raw(aura.holder.cell)
        self.center_x, self.center_y = x, y + radius

    def update(self):
        super().update()

        self.angle += self.rotation
        x, y = cell_to_raw(self.action.holder.cell)
        self.center_x = x + math.cos(self.angle) * self.radius
        self.center_y = y + math.sin(self.angle) * self.radius


class HealingAuraPhysics(AuraPhysics):
    parameters = {"radius": 20,
                  "sprite_pic": "sprite_pictures/healing_aura.png",
                  "sprite_scale": 0.02}

    def __init__(self, aura):
        super().__init__(aura, **HealingAuraPhysics.parameters)
