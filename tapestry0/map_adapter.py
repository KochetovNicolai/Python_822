import sys
import os
from contextlib import contextmanager
import config
from map_generator import map_generator

for_mapping = None


class Cell:
    def __init__(self, x, y, height, state=None):
        self.x = x
        self.y = y
        self.height = height
        self.state = state  # the cell is aware of what is on it

    def __repr__(self):
        return repr((self.x, self.y, self.height))

    def is_occupied(self):
        return self.state is not None

    def reset(self):
        self.state = None


@contextmanager
def replace_message():
    with open(os.devnull, "w") as devnull:
        print("Your map is being generated...")
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            print("Done!")


def generate_map(x=25, y=15, continents=1):
    config.CELL_COUNT_X = x
    config.CELL_COUNT_Y = y
    config.SCREEN_WIDTH = config.CELL_COUNT_X * config.CELL_SIZE
    config.SCREEN_HEIGHT = config.CELL_COUNT_Y * config.CELL_SIZE
    with replace_message():
        map_generator(x, y, continents, "map_files/map")
    generate_heights_map()


def generate_heights_map():
    global for_mapping
    with open(config.MAP_FILE, 'r') as MAP:  # reading cell heights from MAP_FILE
        height = {}
        for k, line in enumerate(MAP):
            height[k] = list(map(int, line.split()))
        for_mapping = {(i, j): Cell(i, j, height[i][config.CELL_COUNT_Y - j - 1])
                       for i in range(config.CELL_COUNT_X)
                       for j in range(config.CELL_COUNT_Y)}
