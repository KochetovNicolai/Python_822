# event_manager deals with the dynamic aspect of game logic - the event loop and other activities

from object_manager import participates, create_unit_object
from classes import Unit
from mapping import get_cell, set_cell, grid_to_cell, cell_to_grid, is_water, cab_distance
from tech_bits import Singleton
from action import Dummy
import UI


# a singleton for managing all in-game events
class Events(metaclass=Singleton):
    def __init__(self):
        self.actors = {}  # dict containing actors' lifespans (None if actor = player's unit)
        self.living_units = set()  # facilitates checking currently living playable units
        self.turns = self.turn_loop()  # event loop itself
        self.current_actor = next(self.turns)  # actor during the current turn

    def turn_loop(self):
        while True:
            if self.actors == {}:
                yield None
            for actor in self.actors:
                if participates(actor):
                    yield actor
                else:
                    continue
                if self.actors[actor] is not None:  # decreases lifespan of temporary actors, kills them when necessary
                    if self.actors[actor] == 1:
                        self.actors.pop(actor)
                    else:
                        self.actors[actor] -= 1

    def add_actor(self, actor, lifespan=None):
        self.actors[actor] = lifespan
        if lifespan is None:
            self.living_units.add(actor)

    def kill_unit(self, unit):
        self.living_units.remove(unit)

    def next_(self):
        self.current_actor = next(self.turns)

    def current_(self):
        return self.current_actor

    def update(self):
        if end_turn(self.current_actor):
            reset(self.current_actor)  # resets all turn-related stats
            self.next_()


# -----------------
# -----------------
# -----------------

# interface connecting to the main.py

def initialise():
    if Events().actors == {}:  # no game possible without actors
        raise Exception
    else:
        Events().next_()


def current_turn():
    return Events().current_()


def next_turn():
    Events().next_()


def update():
    return Events().update()


def winner():
    if len(Events().living_units) == 1:
        return list(Events().living_units)[0]
    else:
        return None


# -----------------
# -----------------
# -----------------

# differs from object_manager.States in that Activity is related more to actions,
# whereas States are primarily about passive effects
class Activity:
    def __init__(self, speed, actions):
        self.speed = speed
        self.steps = speed  # at the moment each cell costs its height in steps to get to it
        self.actions = actions

    def make_step(self, cost):  # on movement
        self.steps -= cost

    def make_action(self, cost):  # on making some action
        self.actions -= cost

    def set(self, *, speed=None, steps=None, actions=None):
        if speed is not None:
            self.speed = speed
        if steps is not None:
            self.steps = steps
        if actions is not None:
            self.actions = actions

    def end_turn(self):
        if self.steps <= 0 or self.actions <= 0:
            return True
        else:
            return False


# resets turn-related stats
def reset(actor):
    actor.activity.set(steps=actor.stats.speed, actions=actor.stats.actions)


def end_turn(actor):
    if isinstance(actor, Unit):  # checker which might be useful in the future if NPCs are implemented
        return actor.activity.end_turn()


# attaches creation to the event loop
def create_unit(x, y, name, type):
    unit = create_unit_object(x, y, name, type)
    unit.activity = Activity(unit.stats.speed, unit.stats.actions)
    Events().add_actor(unit)
    return unit


# object moves in key's direction
def move(obj, key):
    if isinstance(obj, Unit):  # checker which might be useful in the future if NPCs are implemented
        cell = get_cell(obj)
        x, y = cell_to_grid(cell)
        new_cell = None
        if key == UI.MOVE_KEY_RIGHT:
            new_cell = grid_to_cell(x + 1, y)
        elif key == UI.MOVE_KEY_DOWN:
            new_cell = grid_to_cell(x, y - 1)
        elif key == UI.MOVE_KEY_LEFT:
            new_cell = grid_to_cell(x - 1, y)
        elif key == UI.MOVE_KEY_UP:
            new_cell = grid_to_cell(x, y + 1)

        if new_cell is None:
            pass
        elif not is_water(new_cell):
            obj.activity.make_step(new_cell.height)  # attached in def create_unit() here line 106
            cell.state = None
            new_cell.state = obj
            set_cell(obj, new_cell)


def create_attack(actor, cell):
    if get_cell(actor) == cell or cab_distance(get_cell(actor), cell) > actor.stats.vision:
        # impossible to attack further than one's vision allows
        return Dummy()  # described in action.py
    else:
        actor.activity.make_action(1)  # for now the cost of every attack is 1
        return actor.attack(cell)


def hit_actor(actor, action):
    if actor is None or action is None:
        pass
    else:
        actor.stats.hp -= action.modifiers.damage
        if actor.stats.hp <= 0:
            actor.kill()
            if isinstance(actor, Unit):  # specifically to deal with player units
                Events().kill_unit(actor)
