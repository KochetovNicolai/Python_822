from Generator import Generator
from Labyrinth import Labyrinth
import random


# Labyrinth generator that uses DFS algorithm
# Simply runs backtracking non-recursive DFS, selecting random walls
class DFSGenerator(Generator):
    def generate(self, n, m):
        labyrinth = Labyrinth(n, m)
        visited = {(0, 0)}
        stack = [(0, 0)]
        while len(stack) > 0:
            cur_v = stack[-1]

            adj = labyrinth.adjacent(cur_v)
            adj_not_visited = [u for u in adj if u not in visited]

            if len(adj_not_visited) == 0:
                stack.pop()
            else:
                next_v = random.choice(adj_not_visited)
                labyrinth.remove_wall(cur_v, next_v)
                visited.add(next_v)
                stack.append(next_v)

        return labyrinth
