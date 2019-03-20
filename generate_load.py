from Maze import Maze, Cell
from dfs_generator import dfs_generator
from prim_algorithm import prim_algorithm


def generate(maze: Maze, alg, rand='not_rand'):
        if alg == 'prim':
            if rand == 'rand' or rand == 'not_rand':
                prim_algorithm(maze, rand)
            else:
                raise SyntaxError
        elif alg == 'dfs':
            if rand == 'rand' or rand == 'not_rand':
                dfs_generator(maze, rand)
            else:
                raise SyntaxError
        else:
            raise SyntaxError


def load_maze(file):
    f = open(file, 'r')
    line = f.readline().strip('\n').strip()
    width = len(line) // 3 + 1
    maze = Maze(width, -1)
    f.close()
    f = open(file, 'r')

    line_num = -1
    for line in f:
        if line == '\n':
           break
        line.strip('\n').strip()
        line_num += 1
        maze.matrix.append(['WALL' for i in range(width)])
        maze.height += 1
        for i in range(width):
            if line[i * 3] == '#':
                maze.matrix[line_num][i] = 'WALL'
            elif line[i * 3] == '.':
                maze.matrix[line_num][i] = 'SPACE'
            elif line[i * 3] == '/':
                maze.matrix[line_num][i] = 'SPACE'
                if maze.entry is None:
                    maze.entry = Cell(line_num, i)
                else:
                    maze.exit = Cell(line_num, i)
            else:
                raise SyntaxError
    maze.height += 1
    f.close()
    if maze.entry is None or maze.exit is None:
        maze.find_doors()
    return maze
