import random
from Maze import Maze, Cell


def get_divided(cell, maze, used, divided):
    # записывает в divided непосещённые клетки, соседствующие со стеной
    x = cell.x
    y = cell.y
    if used[x + 1][y] == 0 and maze.matrix[x+1][y] == 'SPACE':
        divided.append(Cell(x + 1, y))
    if used[x][y + 1] == 0 and maze.matrix[x][y+1] == 'SPACE':
        divided.append(Cell(x, y + 1))
    if used[x - 1][y] == 0 and maze.matrix[x-1][y] == 'SPACE':
        divided.append(Cell(x - 1, y))
    if used[x][y - 1] == 0 and maze.matrix[x][y-1] == 'SPACE':
        divided.append(Cell(x, y - 1))


def add_walls(cell, maze, walls):
    # добавляет в walls внутренние стены лабиринта, соседние с cell
    x = cell.x
    y = cell.y
    if x + 1 < maze.height - 1 and maze.matrix[x+1][y] == 'WALL':
        walls.append(Cell(x+1, y))
    if y + 1 < maze.width - 1 and maze.matrix[x][y+1] == 'WALL':
        walls.append(Cell(x, y+1))
    if x - 1 >= 1 and maze.matrix[x-1][y] == 'WALL':
        walls.append(Cell(x-1, y))
    if y - 1 >= 1 and maze.matrix[x][y-1] == 'WALL':
        walls.append(Cell(x, y-1))


def prim_algorithm(maze: Maze, rand):
    used = []
    for i in range(maze.height):
        used.append([0 for i in range(maze.width)])
    used[1][1] = 1

    walls = [Cell(2, 1), Cell(1, 2)]
    while len(walls) > 0:
        num = random.randint(0, len(walls) - 1)
        divided = []
        get_divided(walls[num], maze, used, divided)
        if len(divided) == 1:
            used[divided[0].x][divided[0].y] = 1
            maze.set(walls[num], 'SPACE')
            add_walls(divided[0], maze, walls)
        divided.clear()
        walls.pop(num)

    maze.set_doors(rand)
