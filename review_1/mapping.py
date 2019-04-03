# all functions in this module return None (or just pass) when no logical action should be performed
#   for instance, when the object is None, it isn't connected to any cell => get_cell(object) returns None
# there're 3 coordinate systems in use in the project: raw (x, y) coming as input in main.py, grid (i, j) and cells

import UI
from arcade import draw_commands
from math import atan, degrees

MAP_FILE = "map_files/map.txt"
MAP_BACKGROUND = "map_files/map.png"


# draws the map
def draw_background():
    map_texture = draw_commands.load_texture(MAP_BACKGROUND)
    draw_commands.draw_texture_rectangle(center_x=UI.SCREEN_WIDTH / 2, center_y=UI.SCREEN_HEIGHT / 2,
                                         width=UI.SCREEN_WIDTH,
                                         height=UI.SCREEN_HEIGHT, texture=map_texture)


# main map unit
class Cell:
    def __init__(self, x, y, height, state=None):
        self.x = x
        self.y = y
        self.height = height
        self.state = state  # the cell is aware of what is on it

    def __repr__(self):
        return repr((self.x, self.y, self.height))

    def is_occupied(self):
        return self.state is None


# returns the cell which obj is on
def get_cell(obj):
    if obj is None:
        return None
    else:
        return obj.cell


# changes obj's cell
def set_cell(obj, cell):
    if obj is None:
        return None
    else:
        obj.cell = cell


# mapping connects the grid and cells
mapping = None
with open(MAP_FILE, 'r') as MAP:  # reading cell heights from MAP_FILE
    height = {}
    for k, line in enumerate(MAP):
        height[k] = list(map(int, line.split()))
    mapping = {(i, j): Cell(i, j, height[i][UI.CELL_COUNT_Y - j - 1]) for i in range(UI.CELL_COUNT_X) for j in
               range(UI.CELL_COUNT_Y)}


# 6 conversion functions

def grid_to_raw(i, j):
    if i < UI.CELL_COUNT_X and j < UI.CELL_COUNT_Y:
        return (i + 0.5) * UI.CELL_SIZE, (j + 0.5) * UI.CELL_SIZE
    else:
        return None


def raw_to_grid(x, y):
    if x <= UI.SCREEN_WIDTH and y <= UI.SCREEN_HEIGHT:
        return x // UI.CELL_SIZE, y // UI.CELL_SIZE
    else:
        return None


def grid_to_cell(i, j):
    if i < UI.CELL_COUNT_X and j < UI.CELL_COUNT_Y:
        return mapping[i, j]
    else:
        return None


def raw_to_cell(x, y):
    return grid_to_cell(*raw_to_grid(x, y))


def cell_to_grid(cell):
    if cell is None:
        return None
    else:
        return cell.x, cell.y


def cell_to_raw(cell):
    return grid_to_raw(*cell_to_grid(cell))


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


# highlights the cell
def highlight(cell, _color=UI.CELL_HIGHLIGHT_COLOR):
    if cell is None:
        pass
    else:
        x, y = grid_to_raw(cell.x, cell.y)
        draw_commands.draw_rectangle_outline(center_x=x, center_y=y, width=UI.CELL_SIZE, height=UI.CELL_SIZE,
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
