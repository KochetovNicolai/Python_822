from Labyrinth import Labyrinth
from collections import deque


# Class for finding path in labyrinth
class LabyrinthSolver:
	def __init__(self, labyrinth = Labyrinth()):
		self.set_labyrinth(labyrinth)

	def set_labyrinth(self, labyrinth):
		self._labyrinth = labyrinth
		self._solved = False
		self._solution = []

	#BFS is used to find path	
	def resolve(self):
		self._solved = True
		self._solution = []
		parent = {}
		visited = {self._labyrinth.v_begin}
		q = deque()
		q.appendleft(self._labyrinth.v_begin)

		while len(q) > 0:
			cur_v = q.pop()

			if cur_v == self._labyrinth.v_end:
					while cur_v != self._labyrinth.v_begin:
						self._solution.append(cur_v)
						cur_v = parent[cur_v]					
					self._solution.append(cur_v)					
					self._solution = [x for x in reversed(self._solution)]
					return

			adj = self._labyrinth.adjacent(cur_v)
			for x in adj:
				if not self._labyrinth.is_wall(x, cur_v) and x not in visited:
					visited.add(x)
					q.appendleft(x)
					parent[x] = cur_v

	def get_solution(self):
		if self._solved == False:
			self.resolve()
		return self._solution

