from arcade import key
from arcade import draw_text
from arcade import draw_commands
from arcade import color

SCREEN_DELTA = 100
TEXT_MESSAGE_DELTA = 100
TEXT_SIZE = 60
SCREEN_WIDTH = 800 + SCREEN_DELTA * 2 + TEXT_MESSAGE_DELTA
SCREEN_HEIGHT = 400 + SCREEN_DELTA * 2


def draw_map():
    map_texture = draw_commands.load_texture("map.jpg")
    draw_commands.draw_texture_rectangle(center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2, width=SCREEN_WIDTH,
                                         height=SCREEN_HEIGHT, texture=map_texture)


def screen_width():
    return SCREEN_WIDTH - SCREEN_DELTA * 2 - TEXT_MESSAGE_DELTA


def screen_height():
    return SCREEN_HEIGHT - SCREEN_DELTA * 2


SPRITE_SCALING_UNIT = 0.1
SPRITE_SCALING_ACTION = 0.05
ACTION_DELTA = 100
RADIUS_OF_MOVEMENT = 100  # не должен превышать SCREEN_DELTA, иначе спрайты вылезают за поле
UNIT_SPEED = 5
ACTION_COUNT_PER_TURN = 3

MOVE_KEYS = {key.UP, key.DOWN, key.LEFT, key.RIGHT}

NEXT_TURN_KEY = key.SPACE


def display_turn(unit):
    draw_text(f"{unit.name}'s\nturn", screen_width() + SCREEN_DELTA - TEXT_MESSAGE_DELTA, 0, color.WHITE, TEXT_SIZE,
              bold=True, italic=True)


# def display_unit_stats(message, number_of_units, unit):
#    delta = SCREEN_HEIGHT / (number_of_units + 1)
#    draw_text(message, screen_width() + SCREEN_DELTA - TEXT_MESSAGE_DELTA, delta * unit, color.WHITE, TEXT_SIZE,
#              bold=True, italic=True)


YOU_WIN_SIZE = 100


def you_win(winner):
    x = 0
    y = 0
    draw_text(f"{winner.upper()} WINS!!!", x, y, color.WHITE, YOU_WIN_SIZE)
