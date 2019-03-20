import random
from Maze import Maze, Cell


def get_neighbours(cell, width, height, used, neighbours: list):
    # записывает в neighbours непосещённых соседей cell
    x = cell.x
    y = cell.y
    if x + 2 < height and used[x+2][y] == 0:
        neighbours.append(Cell(x+2, y))
    if y + 2 < width and used[x][y+2] == 0:
        neighbours.append(Cell(x, y+2))
    if x - 2 >= 0 and used[x-2][y] == 0:
        neighbours.append(Cell(x-2, y))
    if y - 2 >= 0 and used[x][y-2] == 0:
        neighbours.append(Cell(x, y-2))


def dfs_generator(maze: Maze, rand):

    stack = [Cell(1, 1)]
    used = []
    for i in range(maze.height):
        used.append([0 for i in range(maze.width)])
    used[1][1] = 1
    curr = Cell(1, 1)
    while len(stack) > 0:
        neighbours = []
        get_neighbours(curr, maze.width, maze.height, used, neighbours)
        if len(neighbours) > 0:
            stack.append(curr)
            k = neighbours[random.randint(0, len(neighbours) - 1)]
            new = Cell((curr.x + k.x) // 2, (curr.y + k.y) // 2)  # стена между двумя клетками
            maze.set(new, 'SPACE')
            used[k.x][k.y] = 1
            curr = k
        else:
            curr = stack.pop()

    maze.set_doors(rand)
