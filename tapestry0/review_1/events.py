# dynamic aspects of game logic - the event loop and other activities
from object_manager import participates
from classes import Unit
from tech_bits import Singleton


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
                # decreases lifespan of temporary actors, kills them when necessary
                if self.actors[actor] is not None:
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
        return self.steps <= 0 and self.actions <= 0


# resets turn-related stats
def reset(actor):
    actor.activity.set(steps=actor.stats.speed, actions=actor.stats.actions)


def end_turn(actor):
    # checker which might be useful in the future if NPCs are implemented
    if isinstance(actor, Unit):
        return actor.activity.end_turn()
