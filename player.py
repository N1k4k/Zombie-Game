import pygame
from settings import *
from pathlib import Path
from math import atan2, degrees, pi

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, foreground, groups):
		super().__init__(groups)
		self.images = []
		path = Path(r'images\player').glob('**/*')
		for file in path:
			self.images.append(pygame.image.load(file).convert_alpha())

		self.image = self.images[0]
		self.rect = self.image.get_rect(center = pos)

		self.pos = pygame.math.Vector2(self.rect.center)
		self.direction = pygame.math.Vector2(0, 0)
		self.speed = 200

		self.frame_index = 0
		self.rotation = 0
		self.foreground_mask = foreground

		self.health = 100

	def input(self):
		keys = pygame.key.get_pressed()

		# horizontal
		if keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		# vertical
		if keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

	def move(self, dt):
		if self.direction:
			self.direction = self.direction.normalize()

		self.pos += self.direction * self.speed * dt

		if self.pos[0] - 50 < 0 or self.pos[0] + 50 > 5000 or self.pos[1] - 50 < 0 or self.pos[1] + 50 > 5000 \
		or self.foreground_mask.get_at((self.pos[0], self.pos[1] -50)) \
		or self.foreground_mask.get_at((self.pos[0] +50, self.pos[1])) \
		or self.foreground_mask.get_at((self.pos[0], self.pos[1] +50)) \
		or self.foreground_mask.get_at((self.pos[0] -50, self.pos[1])):
			self.pos = self.rect.center
		else:
			self.rect.center = self.pos

	def animate(self, dt):
		if self.direction:
			self.frame_index += dt * 7
			if self.frame_index >= len(self.images):
				self.frame_index = 0

			self.image = self.images[int(self.frame_index)]
		else:
			self.image = self.images[0]
			self.frame_index = 0

	def rotate(self):
		x, y = pygame.mouse.get_pos()

		dx = x - WINDOW_WIDTH /2
		dy = y - WINDOW_HEIGHT /2
		rads = atan2(-dy,dx)
		rads %= 2*pi
		deg = degrees(rads) - 90
		self.rotation = rads

		self.image = pygame.transform.rotate(self.image, deg)

	def update(self, dt, _, __):
		self.input()
		self.move(dt)
		self.animate(dt)
		self.rotate()