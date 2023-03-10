import math

class Cell:
	def __init__(self, position, side):
		self.pos = position
		self.side = side
		self.visited = False
		self.walls = []
		self.neighbours = []

		self.create_walls()

	def create_walls(self):
		# Create the three extra points to complete the cell.
		top_r = (self.pos[0]+self.side, self.pos[1])
		btm_r = (self.pos[0]+self.side, self.pos[1]+self.side)
		btm_l = (self.pos[0], self.pos[1]+self.side)
		# Append walls to the list.
		self.walls.append([self.pos, top_r])
		self.walls.append([btm_l, btm_r])
		self.walls.append([self.pos, btm_l])
		self.walls.append([top_r, btm_r])

	def find_neighbours(self, grid):
		for cell in grid:
			if math.dist(self.pos, cell.pos) == self.side:
				self.neighbours.append(cell)

	def remove_shared_wall(self, cell):
		for wall in self.walls:
			if wall in cell.walls:
				cell.walls.remove(wall)
				self.walls.remove(wall)


def create_grid(width, height, side):
	grid = []
	for i in range(0, height, side):
		for j in range(0, width, side):
			position = (j, i)
			grid.append(Cell(position, side))
	for cell in grid:
		cell.find_neighbours(grid)
	return grid