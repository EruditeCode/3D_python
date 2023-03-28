# Video Walkthrough Link: ####

import pygame
import math
from sys import exit
from maze_ref import maze
from maze_texture_support import Particle

# The main program loop.
def main():
	pygame.init()
	WIDTH, HEIGHT = 1200, 400
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	bg = pygame.Surface((WIDTH, HEIGHT))
	bg.fill((20,20,20))
	ceiling = pygame.Surface((WIDTH//2, HEIGHT//2))
	ceiling.fill((87,82,73))
	floor = pygame.Surface((WIDTH//2, HEIGHT//2))
	floor.fill((171,150,98))

	wall_texture = pygame.image.load('wallpaper.png').convert()
	wall_texture = pygame.transform.scale(wall_texture, (400, 100))

	p1 = Particle((20,20), 500)

	LEFT, RIGHT, FORWARD, REVERSE = False, False, False, False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					LEFT = True
				if event.key == pygame.K_RIGHT:
					RIGHT = True
				if event.key == pygame.K_UP:
					FORWARD = True
				if event.key == pygame.K_DOWN:
					REVERSE = True
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					exit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					LEFT = False
				if event.key == pygame.K_RIGHT:
					RIGHT = False
				if event.key == pygame.K_UP:
					FORWARD = False
				if event.key == pygame.K_DOWN:
					REVERSE = False

		# Updating the particle position and direction based on user input.		
		new_pos = p1.pos		
		if LEFT:
			p1.dir -= 20
		if RIGHT:
			p1.dir += 20
		if FORWARD:
			angle = math.radians(p1.dir/10)
			x = p1.pos[0] + (1 * math.cos(angle))
			y = p1.pos[1] + (1 * math.sin(angle))
			new_pos = (x, y)
		if REVERSE:
			angle = math.radians(p1.dir/10)
			x = p1.pos[0] - (1 * math.cos(angle))
			y = p1.pos[1] - (1 * math.sin(angle))
			new_pos = (x, y)
		p1.update(new_pos, maze)

		# Displaying background, rays, walls and the particle.
		screen.blit(bg, (0, 0))
		screen.blit(ceiling, (WIDTH//2, 0))
		screen.blit(floor, (WIDTH//2, HEIGHT//2))
		for ray in p1.rays:
			pygame.draw.aaline(screen, (240,240,240), ray.pos, ray.terminus, 1)
		for wall in maze:
			if wall in p1.active_walls:
				pygame.draw.line(screen, (255,0,0), wall[0], wall[1], 1)
			else:
				pygame.draw.line(screen, (200,200,200), wall[0], wall[1], 1)
		pygame.draw.circle(screen, (100,255,100), p1.pos, 7)


		slice_w = (WIDTH//2)/len(p1.rays)
		offset = WIDTH//2
		for i, ray in enumerate(p1.rays):
			if ray.terminus[0] == ray.active_wall[0][0]:
				img_start = (abs(ray.terminus[1] - ray.active_wall[0][1]) * 10)
			else:
				img_start = (abs(ray.terminus[0] - ray.active_wall[0][0]) * 10)

			if img_start >= 300:
				img_start -= 300

			h = (10 / ray.corrected_distance)*HEIGHT
			w = (h / 100) * 400
			y = (HEIGHT//2)-(h//2)
			img_start = (img_start / 400) * w
			tmp_img = pygame.transform.scale(wall_texture, (w, h))
			screen.blit(tmp_img, (offset+(i*slice_w), y), (img_start,0,slice_w,h))

		
		pygame.display.update()
		clock.tick(30)


if __name__ == '__main__':
	main()
