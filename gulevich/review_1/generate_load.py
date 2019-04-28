import sys
import os
from Maze import Maze, Cell, State
from dfs_generator import DfsGenerator
from prim_algorithm import PrimGenerator


def generate(width, height, alg, rand='not_rand'):
        try:
            int(width)
            int(height)
        except Exception as e:
            raise ValueError('Третий и четвёртый аргументы должны быть '
                             'целыми числами, большими 1 - это ширина и высота лабиринта')
        width = int(width)
        height = int(height)
        if width <= 1 or height <= 1:
            raise ValueError('Третий и четвёртый аргументы должны быть '
                             'целыми числами, большими 1 - это ширина и высота лабиринта')
        else:
            if alg == 'prim':
                if rand == 'rand' or rand == 'not_rand':
                    if rand == 'rand':
                        rand = True
                    else:
                        rand = False
                    maze = PrimGenerator.create(width, height, rand)
                else:
                    raise ValueError('Пятый аргумент задан некорректно: требуется rand, not_rand или ничего')
            elif alg == 'dfs':
                if rand == 'rand' or rand == 'not_rand':
                    if rand == 'rand':
                        rand = True
                    else:
                        rand = False
                    maze = DfsGenerator.create(width, height, rand)
                else:
                    ValueError('Пятый аргумент задан некорректно: требуется rand, not_rand или ничего')
            else:
                raise ValueError('Второй аргумент задан некорректно: требуется prim или dfs')
        return maze


def load_maze():
    file = sys.argv[2]
    if os.path.exists(file) is True:
        with open(file, 'r') as f:
            line = f.readline().strip('\n').strip()
            width = len(line) // 3 + 1
            maze = Maze(width, -1)

        with open(file, 'r') as f:
            line_num = -1
            for line in f:
                if line == '\n':
                    break
                line.strip('\n').strip()
                line_num += 1
                maze.matrix.append([State.wall for i in range(width)])
                maze.height += 1
                for i in range(width):
                    if line[i * 3] == '#':
                        maze.matrix[line_num][i] = State.wall
                    elif line[i * 3] == '.':
                        maze.matrix[line_num][i] = State.space
                    elif line[i * 3] == '/':
                        maze.matrix[line_num][i] = State.space
                        if maze.entry is None:
                            maze.entry = Cell(line_num, i)
                        else:
                            maze.exit = Cell(line_num, i)
                    else:
                        raise ValueError('Неверный формат представления лабиринта:\nошибка в строке '+str(line_num))
            maze.height += 1
        if maze.entry is None or maze.exit is None:
            try:
                maze.find_doors()
            except ValueError as e:
                print(e)
                raise SystemExit(777)
        return maze
    else:
        raise ValueError('Файл с указанным во 2 аргументе названием не найден в директории проекта')
