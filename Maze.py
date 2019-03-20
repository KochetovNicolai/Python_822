from termcolor import colored
import random


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
            self.matrix.append(['WALL'])
            self.matrix[i] *= self.width
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if i % 2 == 1 & j % 2 == 1:
                    self.matrix[i][j] = 'SPACE'

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
                    str += colored('/  ', 'green', 'on_green')
                elif self.matrix[i][j] == 'SPACE':
                    #str += '\033[93m.  \033[0m'
                    str += colored('.  ', 'yellow', 'on_yellow')
                elif self.matrix[i][j] == 'WALL':
                    #str += '\033[1m\033[94m#  \033[0m'
                    str += colored('#  ', 'blue', 'on_blue')  # attrs=['bold']
                elif self.matrix[i][j] == 'WAY':
                    #str += '\033[91mS  \033[0m'
                    str += colored('S  ', 'red', 'on_red')
            str += '\n'
        return str

    def set_doors(self, rand='rand'):
        if rand == 'rand':
            en = 2 * random.randint(1, (self.height - 3) // 2) + 1

            ex = 2 * random.randint(1, (self.height - 3) // 2) + 1
        else:
            en = 1
            ex = self.height - 2
        self.entry = Cell(en, 0)
        self.exit = Cell(ex, self.width - 1)
        self.set(self.entry, 'SPACE')
        self.set(self.exit, 'SPACE')

    def find_doors(self):
        #  в качестве дверей найдёт ближайшие к углам пустые клетки во внешней стене лабиринта
        itright = 0
        itdown = 0
        min_dist = self.width + self.height + 10
        max_dist = 0
        while itright < self.width:
            if self.matrix[0][itright] == 'SPACE':
                print('right iter found space on top')
                if itright <= min_dist:
                    min_dist = itright
                    self.entry = Cell(0, itright)
                if itright > max_dist:
                    max_dist = itright
                    self.exit = Cell(0, itright)
            if self.matrix[self.height-1][itright] == 'SPACE':
                print('right iter found space on bot')
                if itright + self.height - 1 < min_dist:
                    min_dist = itright + self.height - 1
                    self.entry = Cell(self.height - 1, itright)
                if itright + self.height - 1 >= max_dist:
                    max_dist = itright + self.height - 1
                    self.exit = Cell(self.height - 1, itright)
            itright += 1
        while itdown < self.height:
            if self.matrix[itdown][0] == 'SPACE':
                print('down iter found space on left')
                if itdown < min_dist:
                    min_dist = itdown
                    self.entry = Cell(itdown, 0)
                if itdown >= max_dist:
                    max_dist = itdown
                    self.exit = Cell(itdown, 0)
            if self.matrix[itdown][self.width-1] == 'SPACE':
                print('down iter found space on right')
                if itdown + self.width - 1 <= min_dist:
                    min_dist = itdown + self.width - 1
                    self.entry = Cell(itdown, self.width - 1)
                if itdown + self.width - 1 > max_dist:
                    max_dist = itdown + self.width - 1
                    self.exit = Cell(itdown, self.width - 1)
            itdown += 1
        print(self.entry.x, self.entry.y)
        print(self.exit.x, self.exit.y)
        if self.entry is None:
            raise SyntaxError

    def save(self, file, type='w'):
        f = open(file, type)
        if type == 'a':
            f.write('\n')
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j] == 'SPACE':
                    f.write('.  ')
                if self.matrix[i][j] == 'WALL':
                    f.write('#  ')
                if self.matrix[i][j] == 'WAY':
                    f.write('S  ')
            f.write('\n')
        f.close()
