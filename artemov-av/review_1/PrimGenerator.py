from Generator import Generator
from Labyrinth import Labyrinth
import random


# Labyrinth generator that uses Prim algorithm
# Repeats randomly getting walls from set; 
# if on the one side of wall there is an unvisited tile, then removes this wall and add adjacent walls for the tile
class PrimGenerator(Generator):
    def generate(self, n, m):
        labyrinth = Labyrinth(n, m)
        visited = {(0, 0)}
        walls = {((0, 0), (0, 1)), ((0, 0), (1, 0))}
        while len(walls) > 0:
            cur_wall = random.sample(walls, 1)[0]

            for i in range(2):
                if cur_wall[i] not in visited:
                    visited.add(cur_wall[i])
                    labyrinth.remove_wall(cur_wall[0], cur_wall[1])
                    adj_walls = labyrinth.adjacent_walls(cur_wall[i])
                    for x in adj_walls:
                        if x[0] not in visited or x[1] not in visited:
                            walls.add(x)

            walls.remove(cur_wall)

        return labyrinth
