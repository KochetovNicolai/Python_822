# object_manager deals with objects, cells and everything related to the game's static aspect

from mapping import grid_to_cell, Cell
from classes import *


# differs from event_manager.Activity in that the latter is related more to actions,
#   whereas States are primarily about passive effects
# for now States.participates doesn't serve any real purpose, but when new functionality is introduced,
#   it would check if the actor can take part in the current turn when alive and stunned, for example
class States:
    def __init__(self):
        self.participates = True

    def set(self, *, participates=None):
        if participates is not None:
            self.participates = participates


# returns function object that is used to display cell's occupant state
# (for now cell.state decides what to display)
def display_state_func(cell):
    if isinstance(cell, Cell):
        if cell is None or cell.state is None:
            pass
        else:
            return cell.state.display


# with no consideration for the event loop + attaches passive states
def create_unit_object(x, y, name, type):
    cell = grid_to_cell(x, y)
    unit = None
    if type == "fighter":
        unit = Fighter(cell, name)
    elif type == "mage":
        unit = Mage(cell, name)
    elif type == "craftsman":
        unit = Craftsman(cell, name)
    elif type == "ranger":
        unit = Ranger(cell, name)
    cell.state = unit
    unit.states = States()
    return unit


# checks if the actor can participate in the current turn
# if actor in not a unit, then there's some logical mistake in the rest of the project
def participates(actor):
    if isinstance(actor, Unit):
        return actor.stats.hp > 0 and actor.states.participates
    else:
        raise Exception
