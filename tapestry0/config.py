from math import pi
from arcade import key

MAP_INPUT_LIMIT = {'x': 7, 'y': 7}

CELL_SIZE = 41  # map generator uses this by default
CELL_COUNT_X = None  # grid's x-axis length
CELL_COUNT_Y = None  # grid's y-axis length
SCREEN_WIDTH = None
SCREEN_HEIGHT = None
RIGHT_GAP = 200
UPPER_GAP = 200
MAP_FILE = "map_files/map.txt"
MAP_BACKGROUND = "map_files/map.png"

BOLT_SPEED = 10  # default speed of bolt from action
# default speed limit of bolt from action after slowing down to which the bolt is destroyed
BOLT_SPEED_LIMIT = 0.1
AURA_ROTATION_SPEED = pi / 45
MODIFIERS_DAMAGE_LIMIT = 5
MODIFIERS_HEAL_LIMIT = 1
SPRITE_SCALING_UNIT = 0.08  # default for unit
ACTION_DELTA = CELL_SIZE + 10  # a temporary solution for the problem 2 described in main.py
UNIT_SPEED = CELL_SIZE  # units step across one cell at a time
UNIT_PIC = "sprite_pictures/head.png"

# various keyboard consts
MOVE_KEY_UP = key.UP
MOVE_KEY_DOWN = key.DOWN
MOVE_KEY_LEFT = key.LEFT
MOVE_KEY_RIGHT = key.RIGHT
MOVE_KEYS = {MOVE_KEY_UP, MOVE_KEY_DOWN, MOVE_KEY_LEFT, MOVE_KEY_RIGHT}
MOVE_DIRECTION = {MOVE_KEY_UP: (0, 1), MOVE_KEY_DOWN: (0, -1),
                  MOVE_KEY_LEFT: (-1, 0), MOVE_KEY_RIGHT: (1, 0)}
NEXT_TURN_KEY = key.SPACE

CLASS_NAMES = ("mage", "fighter", "ranger", "craftsman")
