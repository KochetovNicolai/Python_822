from Generator import Generator
from DFSGenerator import DFSGenerator
from PrimGenerator import PrimGenerator
from Labyrinth import Labyrinth
from LabyrinthSolver import LabyrinthSolver


# Class that is used for generating and solving mazes
class Manager:
	def __init__(self):
		self._generator = DFSGenerator()
		self._maze_solver = LabyrinthSolver()

	def set_generator(self, generator):
		self._generator = generator

	def generate_new_maze(self, n, m):
		maze = self._generator.generate(n, m)
		self._maze_solver.set_labyrinth(maze)
		return maze

	def get_solution(self, labyrinth):
		return self._maze_solver.get_solution()
