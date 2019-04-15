from enum import Enum

# Enum for moving in labyrinth
class Move(Enum):
        UP = 1
        RIGHT = 2
        DOWN = 3
        LEFT = 4


class Labyrinth:
    def __init__(self, n=0, m=0):
        self._matrix = [[0 for i in range(m)] for i in range(n)]
        self._n = n
        self._m = m
        self._not_walls = set() # Contains walls that were removed
        self.v_begin = (0, 0) # Begin tile in labyrinth
        self.v_end = (n-1, m-1) # End tile

        def __repr__(self):
            my_str = ""
            for i in range(self._n):
                for k in range(3):
                    for j in range(self._m):
                        if k == 0:
                            if j == 0 and i == 0:
                                my_str += "*"
                            if i == 0:
                                my_str += "---*"
                        if k == 1 and j == 0:
                            my_str += "|"
                        if k == 2 and j == 0:
                            my_str += "*"

                        if k == 1:
                            if ((i, j), (i, j+1)) not in self._not_walls:
                                my_str += "   |"
                            else:
                                my_str += "    "

                        if k == 2:
                            if ((i, j), (i+1, j)) not in self._not_walls:
                                my_str += "---*"
                            else:
                                my_str += "   *"

                    if k != 0 or i == 0:
                        my_str += "\n"

            return my_str

    def is_correct_tile(self, coords): # Check if the tile with coords is in labyrinth
        return coords[0] < self._n and coords[1] < self._m and min(coords[0], coords[1]) >= 0

    def is_border_wall(self, coords1, coords2): # Check if the wall between tiles is on border of labyrinth
        return not self.is_correct_tile(coords1) or not self.is_correct_tile(coords2)

    def is_wall(self, coords1, coords2): # Check if there is a wall between the tiles
        return tuple(sorted((coords1, coords2))) not in self._not_walls

    def adjacent(self, coords): # Returns list with adjacent tiles (walls don't count)
        if not self.is_correct_tile(coords):
            return []

        adj = []
        if coords[0] > 0:
            adj.append((coords[0]-1, coords[1]))
        if coords[0] < self._n-1:
            adj.append((coords[0]+1, coords[1]))
        if coords[1] > 0:
            adj.append((coords[0], coords[1]-1))
        if coords[1] < self._m-1:
            adj.append((coords[0], coords[1]+1))

        return adj

    def adjacent_walls(self, coords): # Returns list with walls around the tile
        if not self.is_correct_tile(coords):
            return []

        adj = self.adjacent(coords)
        return [tuple(sorted((coords, x))) for x in adj if tuple(sorted((coords, x)))
                not in self._not_walls and not self.is_border_wall(coords, x)]

    def remove_wall(self, coords1, coords2): # Removes wall between two tiles
        if not self.is_correct_tile(coords1) or not self.is_correct_tile(coords2):
            return

        self._not_walls.add(tuple(sorted((coords1, coords2))))

    def apply_move(self, coords, move): # Returns None, if move isn't correct, else returns moved tile
        x = coords[0]
        y = coords[1]
        if move == Move.UP:
            x-=1
        elif move == Move.DOWN:
            x+=1
        elif move == Move.RIGHT:
            y+=1
        elif move == Move.LEFT:
            y-=1

        adj_walls = self.adjacent_walls(coords)
        if not self.is_correct_tile((x, y)) or tuple(sorted((coords, (x, y)))) in adj_walls:
            return None
        return (x, y)
