import random
from abc import ABC, abstractmethod
from Maze import Maze, Cell, State
from Maze_generator import MazeGenerator


class PrimGenerator(MazeGenerator):
    used = []
    walls = [Cell(2, 1), Cell(1, 2)]

    @classmethod
    def get_divided(cls, cell, maze):
        # записывает в divided непосещённые клетки, соседствующие со стеной
        divided = []
        x = cell.x
        y = cell.y
        if cls.used[x + 1][y] == 0 and maze.matrix[x+1][y] == State.space:
            divided.append(Cell(x + 1, y))
        if cls.used[x][y + 1] == 0 and maze.matrix[x][y+1] == State.space:
            divided.append(Cell(x, y + 1))
        if cls.used[x - 1][y] == 0 and maze.matrix[x-1][y] == State.space:
            divided.append(Cell(x - 1, y))
        if cls.used[x][y - 1] == 0 and maze.matrix[x][y-1] == State.space:
            divided.append(Cell(x, y - 1))
        return divided

    @classmethod
    def add_walls(cls, cell, maze):
        # добавляет в walls внутренние стены лабиринта, соседние с cell
        x = cell.x
        y = cell.y
        if x + 1 < maze.height - 1 and maze.matrix[x+1][y] == State.wall:
            cls.walls.append(Cell(x+1, y))
        if y + 1 < maze.width - 1 and maze.matrix[x][y+1] == State.wall:
            cls.walls.append(Cell(x, y+1))
        if x - 1 >= 1 and maze.matrix[x-1][y] == State.wall:
            cls. walls.append(Cell(x-1, y))
        if y - 1 >= 1 and maze.matrix[x][y-1] == State.wall:
            cls.walls.append(Cell(x, y-1))

    @classmethod
    @abstractmethod
    def create(cls, width, height, rand):
        maze = Maze(width, height)
        for i in range(maze.height):
            cls.used.append([0 for i in range(maze.width)])
        cls.used[1][1] = 1

        while len(cls.walls) > 0:
            num = random.randint(0, len(cls.walls) - 1)
            divided = cls.get_divided(cls.walls[num], maze)
            if len(divided) == 1:
                cls.used[divided[0].x][divided[0].y] = 1
                maze.set(cls.walls[num], State.space)
                cls.add_walls(divided[0], maze)
            divided.clear()
            cls.walls.pop(num)

        cls.used = []
        cls.walls = [Cell(2, 1), Cell(1, 2)]
        maze.set_doors(rand)
        return maze
