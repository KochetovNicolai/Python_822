# UI contains certain consts and in the future maybe will be the bridge between game logic and main.py

from arcade import key, color, draw_text
from tech_bits import type_validation

CELL_SIZE = 41  # map generator uses this by default
CELL_COUNT_X = 25  # grid's x-axis length
CELL_COUNT_Y = 15  # grid's y-axis length
CELL_HIGHLIGHT_COLOR = (0, 255, 255)
SCREEN_WIDTH = CELL_COUNT_X * CELL_SIZE
SCREEN_HEIGHT = CELL_COUNT_Y * CELL_SIZE


def screen_width():
    return SCREEN_WIDTH


def screen_height():
    return SCREEN_HEIGHT


BOLT_SPEED = 10  # default speed of bolt from action
BOLT_SPEED_LIMIT = 0.1  # default speed limit of bolt from action after slowing down to which the bolt is destroyed
SPRITE_SCALING_UNIT = 0.08  # default for unit
ACTION_DELTA = CELL_SIZE + 10  # a temporary solution for the problem 2 described in main.py
UNIT_SPEED = CELL_SIZE  # units step across one cell at a time

# various keyboard consts
MOVE_KEY_UP = key.UP
MOVE_KEY_DOWN = key.DOWN
MOVE_KEY_LEFT = key.LEFT
MOVE_KEY_RIGHT = key.RIGHT
MOVE_KEYS = {MOVE_KEY_UP, MOVE_KEY_DOWN, MOVE_KEY_LEFT, MOVE_KEY_RIGHT}
NEXT_TURN_KEY = key.SPACE


# displays "player wins" message
def you_win(winner):
    x = 0
    y = 0
    draw_text(f"{winner.upper()} WINS!!!", x, y, color.WHITE, font_size=100)


# below are the functions, responsible for validating user input
def input_number_of_players():
    return type_validation(lambda: int(input()), message="Wrong input - expected a single number")


def input_player_position():
    return type_validation(lambda: tuple(map(int, input().split())),
                           message="Wrong number of coordinates - requires 2",
                           check=lambda x: len(x) == 2)


CLASS_NAMES = ("mage", "fighter", "ranger", "craftsman")


def input_player_type():
    return type_validation(lambda: input(), message="Wrong class name",
                           check=lambda x: x in CLASS_NAMES)
