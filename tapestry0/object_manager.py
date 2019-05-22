# object_manager deals with objects, cells and everything related to the game's static aspect

from classes import Fighter, Ranger, Mage, Craftsman, Unit


# differs from event_manager.Activity in that the latter is related more to actions,
#   whereas States are primarily about passive effects
# for now States.participates doesn't serve any real purpose,
#   but when new functionality is introduced,
#   it would check if the actor can take part in the current turn
#   (when alive and stunned, for example)
class States:
    def __init__(self):
        self.participates = True

    def set(self, *, participates=None):
        if participates is not None:
            self.participates = participates


# with no consideration for the event loop + attaches passive states
def create_unit_object(cell, name, unit_class):
    unit = None
    if unit_class == "fighter":
        unit = Fighter(cell, name)
    elif unit_class == "mage":
        unit = Mage(cell, name)
    elif unit_class == "craftsman":
        unit = Craftsman(cell, name)
    elif unit_class == "ranger":
        unit = Ranger(cell, name)
    cell.state = unit
    unit.states = States()
    return unit


# checks if the actor can participate in the current turn
# if actor is not a unit, then there's some logical mistake in the rest of the project
def participates(actor):
    if isinstance(actor, Unit):
        return actor.stats.hp > 0 and actor.states.participates
    else:
        raise Exception
