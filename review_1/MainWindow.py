import sys
from enum import Enum
from DFSGenerator import DFSGenerator
from PrimGenerator import PrimGenerator
from Labyrinth import *
from LabyrinthSolver import LabyrinthSolver
from Manager import Manager
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QScrollArea, QPushButton, QFrame, QGroupBox, QRadioButton, QLineEdit, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt, QSize


# Widget that paints labyrinth
class MazeWidget(QWidget):
	# Enum for defining workmode: solve maze automatically or let the user solve it
	class WorkMode(Enum):
		AUTO_SOLVE = 1
		MANUAL_SOLVE = 2

	def __init__(self):
		QWidget.__init__(self)
		self._labyrinth = Labyrinth()
		self._labyrinth_solver = LabyrinthSolver(self._labyrinth)
		self._workmode = self.WorkMode.AUTO_SOLVE
		self._cur_pos = self._labyrinth.v_begin

	def set_mode(self, workmode):
		if self._workmode == self.WorkMode.MANUAL_SOLVE and workmode == self.WorkMode.AUTO_SOLVE:
			self._workmode = workmode
			self._cur_pos = self._labyrinth.v_begin
			self.update()
		self._workmode = workmode
		self._cur_pos = self._labyrinth.v_begin

	def move_in_maze(self, move):
		next_pos = self._labyrinth.apply_move(self._cur_pos, move)
		if next_pos is None:
			return

		self._cur_pos = next_pos
		if self._workmode == self.WorkMode.MANUAL_SOLVE:
			self.update()

	def update_labyrinth(self, labyrinth):
		self._labyrinth = labyrinth
		self._labyrinth_solver.set_labyrinth(labyrinth)
		self._cur_pos = self._labyrinth.v_begin
		self.update()

	# Event that is called when the widget should be repainted
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawLabyrinth(qp)
		qp.end()

	def drawLabyrinth(self, qp):
		maze_height = self._labyrinth._n
		maze_width = self._labyrinth._m

		tile_size = self.geometry().width()/(maze_width+6)	
		margin_x = 3*tile_size
		margin_y = max(margin_x, (self.parent().geometry().height()-tile_size*maze_height)/2)
		pen_width = 2
		pen_color = QColor(0, 0, 0)
		solution_color = QColor(0, 255, 0)

		new_height = margin_y*2+tile_size*maze_height
		self.setMinimumHeight(new_height)

		if self._workmode == self.WorkMode.AUTO_SOLVE:
			qp.setPen(QPen(QBrush(solution_color), pen_width))
			path = self._labyrinth_solver.get_solution()
			for i in range(len(path)-1):
				qp.drawLine(margin_x + tile_size/2 + path[i][1]*tile_size, margin_y + tile_size/2 + path[i][0]*tile_size,
					margin_x + tile_size/2 + path[i+1][1]*tile_size, margin_y + tile_size/2 + path[i+1][0]*tile_size)
		elif self._workmode == self.WorkMode.MANUAL_SOLVE:
			qp.setPen(QPen(QBrush(solution_color), pen_width))
			qp.fillRect(margin_x + self._cur_pos[1]*tile_size, margin_y + self._cur_pos[0]*tile_size, tile_size, tile_size, solution_color)

		qp.setPen(QPen(QBrush(pen_color), pen_width))
		qp.drawRect(margin_x, margin_y, tile_size*maze_width, tile_size*maze_height)
		for i in range(maze_height):
			for j in range(maze_width):
				adj_walls = self._labyrinth.adjacent_walls((i, j))
				if ((i, j),(i, j+1)) in adj_walls:
					qp.drawLine(margin_x + (j+1)*tile_size, margin_y + i*tile_size,
						margin_x + (j+1)*tile_size, margin_y + (i+1)*tile_size)
				if ((i, j),(i+1, j)) in adj_walls:
					qp.drawLine(margin_x + j*tile_size, margin_y + (i+1)*tile_size,
						margin_x + (j+1)*tile_size, margin_y + (i+1)*tile_size)


# Panel in the top of windol
class TopPanel(QFrame):
	def __init__(self, maze_widget=None):
		super().__init__()
		self.setMaximumHeight(150)

		self._manager = Manager()
		self._maze_widget = maze_widget

		layout = QHBoxLayout()
		layout.setContentsMargins(20, 20, 20, 20)

		self.add_algorithm_group(layout)
		self.add_mode_group(layout)
		self.add_width_heigth_fields(layout)
		self.add_generate_button(layout)

		self.setLayout(layout)

	def generate_new_maze(self):
		height = int(self._height_field.text())
		width = int(self._width_field.text())
		self._maze_widget.update_labyrinth(self._manager.generate_new_maze(height, width))

	# Method for adding subwidgets in layout
	def add_algorithm_group(self, layout):
		self._DFS_radio = QRadioButton("DFS")
		self._prim_radio = QRadioButton("Prim")
		self._DFS_radio.setChecked(True)
		self._DFS_radio.clicked.connect(lambda f: self._manager.set_generator(DFSGenerator()))
		self._prim_radio.clicked.connect(lambda f: self._manager.set_generator(PrimGenerator()))

		self._algorithm_group = QGroupBox("Choose algorithm")
		group_layout = QVBoxLayout()
		group_layout.addWidget(self._DFS_radio)
		group_layout.addWidget(self._prim_radio)
		self._algorithm_group.setLayout(group_layout)

		layout.addStretch()
		layout.addWidget(self._algorithm_group)
		layout.addStretch()

	# Method for adding subwidgets in layout
	def add_mode_group(self, layout):
		self._auto_radio = QRadioButton("Auto solve")
		self._manual_radio = QRadioButton("Manual")
		self._auto_radio.setChecked(True)
		self._auto_radio.clicked.connect(lambda f: self._maze_widget.set_mode(MazeWidget.WorkMode.AUTO_SOLVE))
		self._manual_radio.clicked.connect(lambda f: self._maze_widget.set_mode(MazeWidget.WorkMode.MANUAL_SOLVE))

		self._mode_group = QGroupBox("Mode")
		group_layout = QVBoxLayout()
		group_layout.addWidget(self._auto_radio)
		group_layout.addWidget(self._manual_radio)
		self._mode_group.setLayout(group_layout)

		layout.addStretch()
		layout.addWidget(self._mode_group)
		layout.addStretch()

	# Method for adding subwidgets in layout
	def add_width_heigth_fields(self, layout):
		layout.addStretch()
		inner_layout = QGridLayout()
		self._width_label = QLabel("Width")
		self._height_label = QLabel("Height")
		self._width_field = QLineEdit()
		self._height_field = QLineEdit()

		inner_layout.addWidget(self._width_label, 0, 0, 1, 1)
		inner_layout.addWidget(self._width_field, 0, 1, 1, 1)
		inner_layout.addWidget(self._height_label, 1, 0, 1, 1)
		inner_layout.addWidget(self._height_field, 1, 1, 1, 1)

		layout.addLayout(inner_layout)

	# Method for adding subwidgets in layout
	def add_generate_button(self, layout):
		layout.addStretch()
		layout.addStretch()

		self._generate_button = QPushButton("Generate!")
		self._generate_button.clicked.connect(lambda f: self.generate_new_maze())

		layout.addWidget(self._generate_button)
		layout.addStretch()

# Central widget in MainWindow
class MainWidget(QWidget):
	def __init__(self):
		super().__init__()
		self._maze_widget = MazeWidget()
		self._maze_widget.setMinimumSize(700, 700)
		self._top_panel = TopPanel(self._maze_widget)

		self._scroll_area = QScrollArea()
		self._maze_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);
		self._scroll_area.setWidgetResizable(True)
		self._scroll_area.setWidget(self._maze_widget)

		layout = QVBoxLayout()
		layout.addWidget(self._top_panel)
		layout.addWidget(self._scroll_area)
		layout.setContentsMargins(0, 0, 0, 0)

		self._scroll_area.show()

		self.setLayout(layout)

	def get_maze_widget(self):
		return self._maze_widget

	def keyPressEvent(self, event):
		key = event.text()
		if key == 'w':
			self._maze_widget.move_in_maze(Move.UP)
		elif key =='d':
			self._maze_widget.move_in_maze(Move.RIGHT)
		elif key =='s':
			self._maze_widget.move_in_maze(Move.DOWN)
		elif key =='a':
			self._maze_widget.move_in_maze(Move.LEFT)


#Class for application window
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self._main_widget = MainWidget()
		self._main_widget.setMinimumSize(700, 700)
		self.setCentralWidget(self._main_widget)
		self.setWindowTitle('Maze generator')
		self.show()

	def update_labyrinth(self, labyrinth):
		self._main_widget.get_maze_widget().update_labyrinth(labyrinth)

	def get_main_widget(self):
		return self._main_widget
		

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())