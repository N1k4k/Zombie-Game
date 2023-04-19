import pygame
from settings import *
from pathlib import Path
from math import atan2, degrees, pi

class Zombie(pygame.sprite.Sprite):
	def __init__(self, pos, foreground, groups):
		super().__init__(groups)
		self.images = []
		path = Path(r'images\zombie').glob('**/*')
		for file in path:
			self.images.append(pygame.image.load(file).convert_alpha())

		self.image = self.images[0]
		self.rect = self.image.get_rect(center = pos)

		self.pos = pygame.math.Vector2(self.rect.center)
		self.direction = pygame.math.Vector2(0, 0)
		self.speed = 100

		self.health = 100

		self.frame_index = 0
		self.foreground_mask = foreground

	def move(self, dt):
		if self.direction:
			self.direction = self.direction.normalize()

		self.pos += self.direction * self.speed * dt

		if self.foreground_mask.get_at((self.pos[0], self.pos[1] -50)) \
		or self.foreground_mask.get_at((self.pos[0], self.pos[1] +50)):
			self.pos.y = self.rect.centery
		else:
			self.rect.centery = self.pos.y

		if self.foreground_mask.get_at((self.pos[0] +50, self.pos[1])) \
		or self.foreground_mask.get_at((self.pos[0] -50, self.pos[1])):
			self.pos.x = self.rect.centerx
		else:
			self.rect.centerx = self.pos.x

	def animate(self, dt):
		if self.direction:
			self.frame_index += dt * 7
			if self.frame_index >= len(self.images):
				self.frame_index = 0

			self.image = self.images[int(self.frame_index)]
		else:
			self.image = self.images[0]
			self.frame_index = 0

	def rotate(self, player_pos):
		dx = self.rect.centerx - player_pos[0]
		dy = self.rect.centery - player_pos[1]
		rads = atan2(-dy,dx)
		rads %= 2*pi

		self.image = pygame.transform.rotate(self.image, degrees(rads) + 90)

	def update(self, dt, player_pos, _):
		distance = [player_pos[0] - self.rect.centerx, player_pos[1] - self.rect.centery]
		norm = distance[0] ** 2 + distance[1] ** 2
		norm *= norm
		try:
			self.direction =  pygame.math.Vector2(distance[0] / norm, distance[1] / norm)
		except:
			pass

		self.move(dt)
		self.animate(dt)
		self.rotate(player_pos)

		if self.health <= 0:
			SCORE[0] += 100
			self.kill()
			del self