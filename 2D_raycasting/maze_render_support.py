import math

class Particle:
	def __init__(self, position, ray_length):
		self.pos = position
		self.ray_length = ray_length
		self.dir = 0
		self.rays = []
		for angle in range(-300, 300, 1):
			ray = Ray(self.pos, angle, self.ray_length)
			self.rays.append(ray)

	def update(self, point, walls):
		self.pos = point
		grouped_walls = self.group_walls(walls)
		for ray in self.rays:
			ray.update(self.pos, self.dir, grouped_walls)

	def group_walls(self, walls):
		distances = []
		for wall in walls:
			dist_a = math.dist(wall[0], self.pos)
			dist_b = math.dist(wall[1], self.pos)
			if dist_a <= dist_b:
				distances.append(dist_a)
			else:
				distances.append(dist_b)
		ordered_walls = [x for _,x in sorted(zip(distances,walls))]
		
		distances = sorted(distances)
		grouped_walls = []
		temp = [ordered_walls[0]]
		for i in range(1, len(distances)-1):
			if distances[i] == distances[i-1]:
				temp.append(ordered_walls[i])
			else:
				grouped_walls.append(temp)
				temp = [ordered_walls[i]]
		grouped_walls.append(temp)
		return grouped_walls


class Ray:
	def __init__(self, position, angle, max_length):
		self.pos = position
		self.init_angle = angle
		self.angle_rad = math.radians(angle/10)
		self.length = max_length
		self.dir = None
		self.terminus = None
		self.distance = self.length
		self.corrected_distance = None

	def update(self, point, direction, grouped_walls):
		self.pos = point
		self.update_direction(direction)
		self.update_terminus(grouped_walls)
		self.update_corrected_distance()

	def update_direction(self, direction):
		a = self.init_angle + direction
		angle = math.radians(a/10)
		self.dir = (math.cos(angle), math.sin(angle))

	def update_corrected_distance(self):
		self.corrected_distance = self.distance * math.cos(self.angle_rad)

	def update_terminus(self, grouped_walls):
		for group in grouped_walls:
			# Need to get the minimum intersection distance from the group of walls.
			distance, min_terminus = self.length, None
			for wall in group:
				x1, y1 = wall[0][0], wall[0][1]
				x2, y2 = wall[1][0], wall[1][1]
				x3, y3 = self.pos[0], self.pos[1]
				x4, y4 = self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]

				divisor = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
				if divisor == 0:
					# Line segment and ray are parallel, therefore no intersection.
					continue

				t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / divisor
				u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / divisor

				# Check that the point is between the line segment start and end point.
				# Check that the point is on the positive part of the ray (not backwards!).
				if t >= 0 and t <= 1 and u > 0:
					x_point = x1 + t * (x2 - x1)
					y_point = y1 + t * (y2 - y1)
					dist_check = math.dist(self.pos, (x_point, y_point))
					if dist_check < distance:
						distance = dist_check
						min_terminus = (x_point, y_point)

			if distance != self.length:
				self.distance = distance
				self.terminus = min_terminus
				return

		point_x = self.pos[0] + self.dir[0] * self.length
		point_y = self.pos[1] + self.dir[1] * self.length
		self.terminus = (point_x, point_y)
		self.distance = self.length
