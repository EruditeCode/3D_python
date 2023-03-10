class Wall:
	def __init__(self, point_a, point_b):
		self.point_a = point_a
		self.point_b = point_b

class Ray:
	def __init__(self, position, direction):
		self.pos = position
		self.dir = direction
		self.intersection = None

	def update(self, point, wall):
		self.update_direction(point)
		self.update_intersection(wall)

	def update_direction(self, point):
		self.dir = (point[0] - self.pos[0], point[1] - self.pos[1])

	def update_intersection(self, wall):
		x1, y1 = wall.point_a[0], wall.point_a[1]
		x2, y2 = wall.point_b[0], wall.point_b[1]
		x3, y3 = self.pos[0], self.pos[1]
		x4, y4 = self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]

		divisor = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
		if divisor == 0:
			# Line segment and ray are parallel, therefore no intersection.
			self.intersection = None
			return

		t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / divisor
		u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / divisor

		# Check that the point is between the line segment start and end point.
		# Check that the point is on the positive part of the ray (not backwards!).
		if t >= 0 and t < 1 and u > 0:
			x_point = x1 + t * (x2 - x1)
			y_point = y1 + t * (y2 - y1)
			self.intersection = (x_point, y_point)
		else:
			self.intersection = None
