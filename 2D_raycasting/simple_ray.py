import pygame
from simple_ray_support import Ray, Wall
from sys import exit

# The main program function.
def main():
	pygame.init()
	WIDTH, HEIGHT = 800, 500
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	bg = pygame.Surface((WIDTH, HEIGHT))
	bg.fill((20,20,20))

	# Create the ray and the wall objects.
	ray = Ray((200, 250), (1, 0))
	w1 = Wall((600, 100), (600, 400))

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		# Update ray object.
		mouse = pygame.mouse.get_pos()
		ray.update(mouse, w1)

		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		# Displaying the ray and ray source.
		ray_terminus = (ray.pos[0] + ray.dir[0], ray.pos[1] + ray.dir[1])
		pygame.draw.aaline(screen, (255,255,255), ray.pos, ray_terminus)
		pygame.draw.circle(screen, (255,255,255), ray.pos, 5)

		# Displaying the wall and intersection point if required.
		if ray.intersection != None:
			pygame.draw.circle(screen, (255,255,255), ray.intersection, 2)
			for i in range(100, 401):
				if i < ray.intersection[1]:
					rgb = 255 - 2*(ray.intersection[1] - i)
				else:
					rgb = 255 - 2*(i - ray.intersection[1])
				if rgb < 100:
					rgb = 100
				pygame.draw.line(screen, (rgb,rgb,rgb), (600, i), (620, i))
		else:
			point_a = (w1.point_a[0]+10, w1.point_a[1])
			point_b = (w1.point_b[0]+10, w1.point_b[1])
			pygame.draw.line(screen, (100,100,100), point_a, point_b, 21)

		pygame.display.update()
		clock.tick(60)


if __name__ == '__main__':
	main()
