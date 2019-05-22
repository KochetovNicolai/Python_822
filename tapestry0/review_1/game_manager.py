from tech_bits import Singleton
from mapping import grid_to_cell
import event_manager
import physics_manager


class Game(metaclass=Singleton):
    def __init__(self):
        self.names_mapping = {}

    def setup(self, names, unit_classes, coordinates):
        for name in names:
            x, y = coordinates[name]
            cell = grid_to_cell(x, y)
            self.names_mapping[name] = create_unit(cell, name, unit_classes[name])
        event_manager.initialise()

    def winner(self):
        if event_manager.winner() is not None:
            winner = event_manager.winner()
            for name, temp in self.names_mapping.items():
                if temp == winner:
                    return name
        return None


def setup(names, unit_classes, coordinates):
    Game().setup(names, unit_classes, coordinates)


def update():
    event_manager.update()


def current_turn():
    return event_manager.current_turn()


def move_current(direction):
    event_manager.move(event_manager.current_turn(), direction)


def next_turn():
    event_manager.next_turn()


def create_unit(cell, name, unit_class):
    unit = event_manager.create_unit(cell, name, unit_class)
    physics_manager.attach_unit_physics(unit)
    return unit


def create_current_attack(cell):
    attack = event_manager.create_attack(event_manager.current_turn(), cell)
    physics_manager.attach_action_physics(attack)
    return attack


def create_current_aura_over(cell):
    aura = event_manager.create_healing_aura(event_manager.current_turn(), cell.state)
    physics_manager.attach_action_physics(aura)
    return aura


def hit_actor(actor, action):
    event_manager.hit_actor(actor, action)


def kill_action(action):
    event_manager.kill_action(action)


def kill_actor(actor):
    event_manager.kill_actor(actor)


def sprite_to_object(sprite):
    return physics_manager.physics_to_object(sprite)


def object_to_sprite(_object):
    return physics_manager.object_to_physics(_object)
