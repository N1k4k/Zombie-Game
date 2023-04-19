import pygame
from settings import *
from math import sin, cos, degrees, pi

class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = pygame.Vector2()
		self.display_surface = pygame.display.get_surface()
		self.bg = pygame.image.load('images/bg.png').convert()
		self.foreground = pygame.image.load("images/foreground.png").convert_alpha()

	def customize_draw(self,player):

		# change the offset vector
		self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

		# blit the surfaces 
		self.display_surface.blit(self.bg,-self.offset)
		for sprite in self.sprites():
			offset_rect = sprite.image.get_rect(center = sprite.rect.center)
			offset_rect.center -= self.offset
			self.display_surface.blit(sprite.image,offset_rect)

		self.display_surface.blit(self.foreground,-self.offset)



class Gun(pygame.sprite.Sprite):
	def __init__(self, src, shoot_speed, groups, foreground, bullet_groups):
		super().__init__(groups)
		self.type = pygame.image.load(src).convert_alpha()
		self.image = self.type
		self.rect = self.image.get_rect(center = (0, 0))

		self.bullet_groups = bullet_groups
		self.bullet_surf = pygame.image.load('images/bullet.png').convert_alpha()
		self.bullet_surf = pygame.transform.scale(self.bullet_surf, (8, 8))
		self.foreground = foreground

		self.speed = shoot_speed
		self.timer = 0

	def update(self, dt, player_pos, player_rotate):
		self.image = self.type
		self.image = pygame.transform.rotate(self.image, degrees(player_rotate))
		self.rect.center = player_pos[0] + sin(player_rotate + pi /2) * 60, player_pos[1] + cos(player_rotate + pi /2) * 60

		self.timer += dt

		if pygame.mouse.get_pressed()[0] and self.timer > self.speed:
			direction = sin(player_rotate + pi/2), cos(player_rotate + pi/2)
			Bullet((self.rect.center), direction, self.bullet_surf, self.foreground, self.bullet_groups)

			self.timer = 0

class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos, direction, surf, foreground, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(center = pos)

		self.pos = pygame.math.Vector2(self.rect.center)
		self.direction = pygame.math.Vector2(direction)
		self.speed = 800
		self.foreground_mask = foreground

	def update(self, dt, player_pos, player_rotate):
		self.pos += self.direction * self.speed * dt
		self.rect.center = self.pos

		if self.rect.x < 0 or self.rect.x > 5000 or self.rect.y < 0 or self.rect.y > 5000:
			self.kill()
			del self
			return

		try:
			if self.foreground_mask.get_at(self.rect.center):
				self.kill()
				del self
		except:
			pass