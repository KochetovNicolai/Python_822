import arcade
from enum import Enum, unique
from collections import deque
import UI


@unique
class EventId(Enum):
    MOVE_EVENT = 1
    SPELL_EVENT = 2


class Event:

    def __init__(self, units):
        self.units = deque(units)
        self.action_count = UI.ACTION_COUNT_PER_TURN
        self.events = []
        self.unit_turns_chain = Event.event_loop(self.units)
        self.current_player = next(self.unit_turns_chain)
        self.new_move_event(self.current_player)

    @staticmethod
    def event_loop(units):
        while True:
            for i in units:
                yield i

    def get_current_player(self):
        return self.current_player

    def pop_event(self):
        return self.events.pop()

    def get_event(self):
        return self.events[len(self.events) - 1]

    def new_move_event(self, unit):
        self.events.append((EventId.MOVE_EVENT, unit))

    def next_unit_turn(self):
        self.action_count = UI.ACTION_COUNT_PER_TURN
        self.current_player = next(self.unit_turns_chain)
        self.new_move_event(self.current_player)

    def kill_unit(self, unit):
        temp = self.current_player
        for event in self.events:
            if event[1] == unit:
                self.events.remove(event)

        self.units.remove(unit)
        index = self.units.index(temp)
        self.units.rotate(index + 1)
        self.unit_turns_chain = Event.event_loop(self.units)

        if len(self.events) == 0:
            self.next_unit_turn()

    def game_over(self):
        return len(self.units) == 1
