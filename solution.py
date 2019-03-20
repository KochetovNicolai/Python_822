import copy
from collections import deque

from Maze import Maze, Cell


def get_next(cell, maze, next):
    # записывает в next соседние с cell пустые клетки
    x = cell.x
    y = cell.y
    if x + 1 < maze.height and maze.matrix[x + 1][y] == 'SPACE':
        next.append(Cell(x + 1, y))
    if y + 1 < maze.width and maze.matrix[x][y + 1] == 'SPACE':
        next.append(Cell(x, y + 1))
    if x - 1 >= 0 and maze.matrix[x - 1][y] == 'SPACE':
        next.append(Cell(x - 1, y))
    if y - 1 >= 0 and maze.matrix[x][y - 1] == 'SPACE':
        next.append(Cell(x, y - 1))


def solution(maze: Maze):
    # решение лабиринта методом bfs
    maze1 = copy.deepcopy(maze)
    if maze1.entry == maze1.exit:
        maze1.set(maze.entry, 'WAY')
        return maze1

    parents = []
    for i in range(maze1.height):
        parents.append([Cell(-2, -2) for i in range(maze1.width)])
    parents[maze1.entry.x][maze1.entry.y] = Cell(-1, -1)

    used = []
    for i in range(maze1.height):
        used.append([0 for i in range(maze1.width)])

    queue = deque()
    queue.appendleft(maze1.entry)
    used[maze.entry.x][maze.entry.y] = 1

    while len(queue) > 0:
        curr = queue.pop()
        if curr == maze1.exit:
            prev = parents[curr.x][curr.y]
            maze1.set(curr, 'WAY')
            while not prev == maze1.entry:
                maze1.set(prev, 'WAY')
                curr = prev
                prev = parents[curr.x][curr.y]
            maze1.set(maze1.entry, 'WAY')
            break

        else:
            next = []
            get_next(curr, maze1, next)
            for i in next:
                if used[i.x][i.y] == 0 and parents[curr.x][curr.y] != i:
                    parents[i.x][i.y] = curr
                    queue.appendleft(i)
                    used[i.x][i.y] = 1
            next.clear()

    if not maze1.get(maze1.exit) == 'WAY':
        print('NO SOLUTION')
    return maze1


# def solution(maze: Maze):
#     maze1 = copy.deepcopy(maze)
#     parents = []
#     for i in range(maze1.height):
#         parents.append([Cell(-2, -2) for i in range(maze1.width)])
#     parents[maze1.entry.x][maze1.entry.y] = Cell(-1, -1)
#
#     used = []
#     for i in range(maze1.height):
#         used.append([0 for i in range(maze1.width)])
#
#     stack = list()
#     stack.append(maze1.entry)
#
#     while len(stack) > 0:
#         curr = stack.pop()
#         if curr == maze1.exit:
#             prev = parents[curr.x][curr.y]
#             maze1.set(curr, 'WAY')
#             while not prev == maze1.entry:
#                 maze1.set(prev, 'WAY')
#                 curr = prev
#                 prev = parents[curr.x][curr.y]
#             maze1.set(maze1.entry, 'WAY')
#             break
#
#         elif used[curr.x][curr.y] == 0:
#             next = []
#             get_next(curr, maze1, next)
#             for i in next:
#                 if used[i.x][i.y] == 0 and parents[curr.x][curr.y] != i:
#                     parents[i.x][i.y] = curr
#                     stack.append(i)
#             next.clear()
#
#         used[curr.x][curr.y] = 1
#
#     if not maze1.get(maze1.exit) == 'WAY':
#         print('NO SOLUTION')
#     return maze1
