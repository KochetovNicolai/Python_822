# event system management

from tech_bits import Dummy
from classes import Unit
from events import Events, Activity, reset
from mapping import get_cell, cell_to_grid, grid_to_cell, is_water, set_cell, cab_distance
from object_manager import create_unit_object
import action_manager


def initialise():
    if Events().actors == {}:  # no game possible without actors
        raise Exception
    else:
        Events().next_()


def current_turn():
    return Events().current_()


def next_turn():
    reset(current_turn())
    Events().next_()


def update():
    Events().update()


def winner():
    if len(Events().living_units) == 1:
        return list(Events().living_units)[0]
    else:
        return None


# attaches creation to the event loop
def create_unit(cell, name, unit_class):
    unit = create_unit_object(cell, name, unit_class)
    unit.activity = Activity(unit.stats.speed, unit.stats.actions)
    Events().add_actor(unit)
    return unit


def move(obj, direction):
    if isinstance(obj, Unit):  # checker which might be useful in the future if NPCs are implemented
        cell = get_cell(obj)
        x, y = cell_to_grid(cell)
        new_cell = grid_to_cell(x + direction[0], y + direction[1])

        if new_cell is None or new_cell.is_occupied():
            pass
        elif not is_water(new_cell) and new_cell.height <= obj.activity.steps:
            obj.activity.make_step(new_cell.height)  # attached in def create_unit()
            cell.reset()
            new_cell.state = obj
            set_cell(obj, new_cell)


# object moves in key's direction
def create_attack(actor, cell):
    # impossible to attack further than one's vision allows
    if cab_distance(get_cell(actor), cell) > actor.stats.vision\
            or actor.activity.actions == 0\
            or get_cell(actor) == cell:
        return Dummy()  # described in tech_bits.py
    else:
        actor.activity.make_action(1)  # for now the cost of every attack is 1
        return actor.attack(cell)


def create_healing_aura(actor, _object):
    if not isinstance(_object, Unit)\
            or actor.activity.actions == 0\
            or cab_distance(get_cell(actor), get_cell(_object)) > actor.stats.vision:
        return Dummy()
    else:
        actor.activity.make_action(1)
        return action_manager.create_heal_action("healing aura", _object)


def kill_actor(actor):
    if isinstance(actor, Unit):  # specifically to deal with player units
        Events().kill_unit(actor)
    actor.kill()


def kill_action(action):
    action_manager.kill_action(action)


def hit_actor(actor, action):
    if actor is None or action is None:
        pass
    else:
        actor.stats.hp -= action.modifiers.damage
        if actor.stats.hp <= 0:
            kill_actor(actor)
