
class Puzzle:
	def __init__(self, grid):
		self.__grid = grid
		self.heuristic = 0
		self.gn = 0

	def __str__(self):
		str_grid = "\n"
		for row in self.__grid:
			for col in row:
				str_grid += str(col) + " "
			str_grid += "\n"

		return str_grid

	'''					 '''
	'''	Public functions '''
	'''					 '''

	def get_size(self):
		return len(self.__grid)

	def is_solved(self, goal):
		return self.__grid == goal

	def expand(self, puzzles_tried):
		nodes = []
		row, col = self.locate_b()

		if(self.__can_shift_up()):
			puzzle = Puzzle(self.__shift_up())
			puzzle.set_gn(self.gn + 1)

			#	Check if we already tried this puzzle or else we risk looping forever on some puzzles
			puzzle_try = tuple(puzzle.get_grid_1d())
			if(puzzle_try not in puzzles_tried):
				nodes.append(puzzle)
				puzzles_tried.add(puzzle_try)

		if(self.__can_shift_down()):
			puzzle = Puzzle(self.__shift_down())
			puzzle.set_gn(self.gn + 1)

			#	Check if we already tried this puzzle or else we risk looping forever on some puzzles
			puzzle_try = tuple(puzzle.get_grid_1d())
			if(puzzle_try not in puzzles_tried):
				nodes.append(puzzle)
				puzzles_tried.add(puzzle_try)


		if(self.__can_shift_left()):
			puzzle = Puzzle(self.__shift_left())
			puzzle.set_gn(self.gn + 1)

			#	Check if we already tried this puzzle or else we risk looping forever on some puzzles
			puzzle_try = tuple(puzzle.get_grid_1d())
			if(puzzle_try not in puzzles_tried):
				nodes.append(puzzle)
				puzzles_tried.add(puzzle_try)


		if(self.__can_shift_right()):
			puzzle = Puzzle(self.__shift_right())
			puzzle.set_gn(self.gn + 1)

			#	Check if we already tried this puzzle or else we risk looping forever on some puzzles
			puzzle_try = tuple(puzzle.get_grid_1d())
			if(puzzle_try not in puzzles_tried):
				nodes.append(puzzle)
				puzzles_tried.add(puzzle_try)


		return nodes, puzzles_tried


	def is_near(self, number):
		#	Assume that point is not in our view distance (above, below, left, right)	
		ret = 0
		#	Get points nearby
		pts = self.nearby_pts()
		#	Check if pts match with given number
		for point in pts:
			row = point[0]
			col = point[1]
			if (self.__grid[row][col] == str(number)):
				ret = 1

		return ret

	def nearby_pts(self):
		n = len(self.__grid)
		#	Here we will store pts that we will return
		pts = []
		#	Get location of blank space
		row, col = self.locate_b()
		#	Make sure that pts are in our view distance (above, below, left, right)
		#	Make sure we are not giving pts that are outside of grid
		if (row != 0):
			pt_above = [row-1, col]
			pts.append(pt_above)

		if (row != n-1):
			pt_below = [row+1, col]
			pts.append(pt_below)

		if (col != 0):
			pt_left = [row, col-1]
			pts.append(pt_left)

		if (col != n-1):
			pt_right = [row, col+1]
			pts.append(pt_right)

		return pts


	def get_grid(self):
		temp_grid = []

		for row in self.__grid:
			rows = []
			for col in row:
				rows.append(col)
			temp_grid.append(rows)

		return temp_grid

	def get_grid_1d(self):
		temp_grid = []

		for row in self.__grid:
			for col in row:
				temp_grid.append(col)

		return temp_grid		

	def locate_b(self):
		n = len(self.__grid)
		for row in range(n):
			for col in range(n):
				if (self.__grid[row][col] == 'b'):
					return row, col

	def get_heuristic(self):
		return int(self.heuristic)

	def set_heuristic(self, h):
		self.heuristic = h

	def get_gn(self):
		return int(self.gn)

	def set_gn(self, gn):
		self.gn = gn

	'''					  '''
	'''	Private functions '''
	'''					  '''

	def __can_shift_up(self):
		is_success = 0
		row, col = self.locate_b()

		#	Check if the location of the blank space is at the top of the grid
		if (row != 0):
			is_success = 1
		
		return is_success

	def __can_shift_down(self):
		is_success = 0
		row, col = self.locate_b()
		n = len(self.__grid)

		#	Check if the location of the blank space is at the bottom of the grid
		if (row != n-1):
			is_success = 1
		
		return is_success

	def __can_shift_left(self):
		is_success = 0
		row, col = self.locate_b()

		#	Check if the location of the blank space is at the left of the grid
		if (col != 0):
			is_success = 1
		
		return is_success

	def __can_shift_right(self):
		is_success = 0
		row, col = self.locate_b()
		n = len(self.__grid)

		#	Check if the location of the blank space is at the right of the grid
		if (col != n-1):
			is_success = 1
		
		return is_success

	def __shift_up(self):
		row, col = self.locate_b()
		temp_grid = self.get_grid()

		temp = temp_grid[row][col]
		temp_grid[row][col] = temp_grid[row-1][col]
		temp_grid[row-1][col] = temp

		return temp_grid

	def __shift_down(self):
		row, col = self.locate_b()
		temp_grid = self.get_grid()
		
		temp = temp_grid[row][col]
		temp_grid[row][col] = temp_grid[row+1][col]
		temp_grid[row+1][col] = temp

		return temp_grid

	def __shift_left(self):
		row, col = self.locate_b()
		temp_grid = self.get_grid()

		temp = temp_grid[row][col]
		temp_grid[row][col] = temp_grid[row][col-1]
		temp_grid[row][col-1] = temp

		return temp_grid

	def __shift_right(self):
		row, col = self.locate_b()
		temp_grid = self.get_grid()

		temp = temp_grid[row][col]
		temp_grid[row][col] = temp_grid[row][col+1]
		temp_grid[row][col+1] = temp

		return temp_grid

