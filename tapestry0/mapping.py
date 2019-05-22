# all functions in this module return None (or just pass) when no logical action should be performed
#   for instance, when the object is None, it isn't connected to any cell
#   => get_cell(object) returns None
# there're 3 coordinate systems in use in the project:
#   raw (x, y) coming as input in main.py, grid (i, j) and cells

from math import atan, degrees
from arcade import draw_commands, text, color
import config
import map_adapter


# returns the cell that obj belongs to
def get_cell(obj):
    if obj is None:
        return None
    elif isinstance(obj, map_adapter.Cell):
        return obj
    else:
        return obj.cell


# changes obj's cell
def set_cell(obj, cell):
    if obj is None:
        return None
    elif isinstance(obj, map_adapter.Cell):
        obj = cell
    else:
        obj.cell = cell


# 6 conversion functions

def grid_to_raw(i, j):
    if 0 <= i < config.CELL_COUNT_X and 0 <= j < config.CELL_COUNT_Y:
        return (i + 0.5) * config.CELL_SIZE, (j + 0.5) * config.CELL_SIZE
    else:
        return None


def raw_to_grid(x, y):
    if 0 <= x <= config.SCREEN_WIDTH and 0 <= y <= config.SCREEN_HEIGHT:
        return x // config.CELL_SIZE, y // config.CELL_SIZE
    else:
        return None


def grid_to_cell(i, j):
    if 0 <= i < config.CELL_COUNT_X and 0 <= j < config.CELL_COUNT_Y:
        return map_adapter.for_mapping[i, j]
    else:
        return None


def raw_to_cell(x, y):
    if raw_to_grid(x, y) is not None:
        return grid_to_cell(*raw_to_grid(x, y))
    else:
        return None


def cell_to_grid(cell):
    if cell is None:
        return None
    else:
        return cell.x, cell.y


def cell_to_raw(cell):
    if cell is not None:
        return grid_to_raw(*cell_to_grid(cell))
    else:
        return None


def cab_distance(cell1, cell2):
    if cell1 is None or cell2 is None:
        return None
    else:
        return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)


# angle between (cell1, cell2) vector and the x-axis
def angle(cell1, cell2):
    if cell1 is None or cell2 is None:
        return None
    else:
        x1, y1 = cell_to_grid(cell1)
        x2, y2 = cell_to_grid(cell2)
        if x2 - x1 > 0:
            return degrees(atan((y2 - y1) / (x2 - x1)))
        elif x2 - x1 < 0:
            return 180 + degrees(atan((y2 - y1) / (x2 - x1)))
        elif y2 - y1 > 0:
            return 90
        elif y2 - y1 < 0:
            return -90
        else:
            raise Exception


CELL_HIGHLIGHT_COLOR = (0, 255, 255)


# highlights the cell
def highlight(cell, _color=CELL_HIGHLIGHT_COLOR):
    if cell is None:
        pass
    else:
        x, y = cell_to_raw(cell)
        draw_commands.draw_rectangle_outline(center_x=x, center_y=y,
                                             width=config.CELL_SIZE, height=config.CELL_SIZE,
                                             color=_color, border_width=5)


def is_water(cell):
    if cell is None:
        return None
    else:
        return cell.height < 2


def is_rocky(cell):
    if cell is None:
        return None
    else:
        return cell.height > 3


def nearby_cells(cell):
    if cell is not None:
        for direction in config.MOVE_DIRECTION.values():
            x, y = cell_to_grid(cell)
            new_cell = grid_to_cell(x + direction[0], y + direction[1])
            if new_cell is not None:
                yield new_cell


def display_height(cell):
    if cell is not None:
        x, y = cell_to_raw(cell)
        output = cell.height
        if output <= 1:
            output = "X"
        text.draw_text(f"{output}", x - config.CELL_SIZE / 5, y - config.CELL_SIZE / 3,
                       color.GOLD, 30)
