from termcolor import colored
import random
from enum import Enum


class State(Enum):
    wall = 1
    space = 2
    way = 3


class Cell:
    def __init__(self, x_=0, y_=0):
        self.x = x_
        self.y = y_

    def __eq__(self, other):
        if isinstance(other, Cell):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            return False


class Maze:
    def __init__(self, width, height):
        # чтобы лабиринт был красивым - измерения должны быть нечётными
        if width % 2 == 0:
            self.width = width + 1
        else:
            self.width = width
        if height % 2 == 0:
            self.height = height + 1
        else:
            self.height = height

        # свободные клетки разделены стенами
        self.matrix = []
        for i in range(self.height):
            self.matrix.append([State.wall for i in range(self.width)])
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if i % 2 == 1 & j % 2 == 1:
                    self.matrix[i][j] = State.space

        self.entry = None
        self.exit = None

    def get(self, cell: Cell):
        return self.matrix[cell.x][cell.y]

    def set(self, cell: Cell, value):
        self.matrix[cell.x][cell.y] = value

    def __str__(self):
        str = ''
        for i in range(self.height):
            for j in range(self.width):
                if self.entry == Cell(i, j) or self.exit == Cell(i, j):
                    str += colored('/  ', 'yellow', 'on_green')
                elif self.matrix[i][j] == State.space:
                    #str += '\033[93m.  \033[0m'
                    str += colored('.  ', 'yellow', 'on_yellow')
                elif self.matrix[i][j] == State.wall:
                    #str += '\033[1m\033[94m#  \033[0m'
                    str += colored('#  ', 'blue', 'on_blue')  # attrs=['bold']
                elif self.matrix[i][j] == State.way:
                    #str += '\033[91mS  \033[0m'
                    str += colored('S  ', 'red', 'on_red')
            str += '\n'
        return str

    def set_doors(self, rand):
        if rand is True:
            en = 2 * random.randint(1, (self.height - 3) // 2) + 1

            ex = 2 * random.randint(1, (self.height - 3) // 2) + 1
        else:
            en = 1
            ex = self.height - 2
        self.entry = Cell(en, 0)
        self.exit = Cell(ex, self.width - 1)
        self.set(self.entry, State.space)
        self.set(self.exit, State.space)

    def find_doors(self):
        #  в качестве дверей найдёт ближайшие к углам пустые клетки во внешней стене лабиринта
        itright = 0
        itdown = 0
        min_dist = self.width + self.height + 10
        max_dist = 0
        while itright < self.width:
            if self.matrix[0][itright] == State.space:
                if itright <= min_dist:
                    min_dist = itright
                    self.entry = Cell(0, itright)
                if itright > max_dist:
                    max_dist = itright
                    self.exit = Cell(0, itright)
            if self.matrix[self.height-1][itright] == State.space:
                if itright + self.height - 1 < min_dist:
                    min_dist = itright + self.height - 1
                    self.entry = Cell(self.height - 1, itright)
                if itright + self.height - 1 >= max_dist:
                    max_dist = itright + self.height - 1
                    self.exit = Cell(self.height - 1, itright)
            itright += 1
        while itdown < self.height:
            if self.matrix[itdown][0] == State.space:
                if itdown < min_dist:
                    min_dist = itdown
                    self.entry = Cell(itdown, 0)
                if itdown >= max_dist:
                    max_dist = itdown
                    self.exit = Cell(itdown, 0)
            if self.matrix[itdown][self.width-1] == State.space:
                if itdown + self.width - 1 <= min_dist:
                    min_dist = itdown + self.width - 1
                    self.entry = Cell(itdown, self.width - 1)
                if itdown + self.width - 1 > max_dist:
                    max_dist = itdown + self.width - 1
                    self.exit = Cell(itdown, self.width - 1)
            itdown += 1
        if self.entry is None:
            raise ValueError('Двери не найдены')

    def save(self, file, type='w'):
        with open(file, type) as f:
            if type == 'a':
                f.write('\n')
            for i in range(self.height):
                for j in range(self.width):
                    if self.matrix[i][j] == State.space:
                        f.write('.  ')
                    if self.matrix[i][j] == State.wall:
                        f.write('#  ')
                    if self.matrix[i][j] == State.way:
                        f.write('S  ')
                f.write('\n')
