import pygame, sys
from settings import *
from player import Player
from zombie import Zombie
from assets import *
from random import choice, randint
from menu import *

pygame.init()
clock = pygame.time.Clock()

# game
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Zombie Survival')

foreground = pygame.image.load("images/foreground.png").convert_alpha()
foreground_mask = pygame.mask.from_surface(foreground)

font = pygame.font.SysFont("", 60)
highscore_file = open("highscore.txt", "r")
HIGHSCORE = int(highscore_file.read())

all_sprites = AllSprites()
bullet_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()

player = Player((2500, 3000), foreground_mask, all_sprites)
gun = Gun("images/ak.png", 0.15, all_sprites, foreground_mask, [all_sprites, bullet_group])

wave = 1

# spawns zombies
for i in range(8):
	coords = ([2750, 500], [2700, 4500], [500, 2500], [4500, 2500])
	pos = choice(coords)
	pos[0] += randint(-300, 300)
	pos[1] == randint(-300, 300)
	Zombie(pos, foreground_mask,[all_sprites, zombie_group])

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE and player.health <= 0:
				player.kill()
				player = Player((2500, 3000), foreground_mask, all_sprites)
				for z in zombie_group: z.kill()
				wave = 0
				SCORE[0] = 0

	dt = clock.tick(30) /1000

	# update
	display_surface.fill((0, 100, 150))

	# chech if every zombie is killed
	if len(zombie_group) == 0:
		wave += 1
		for i in range(8 * wave):
			coords = ([2500, 500], [2500, 4500], [500, 2500], [4500, 2500])
			pos = choice(coords)
			pos[0] += randint(-100, 100)
			pos[1] == randint(-100, 100)
			Zombie(pos, foreground_mask,[all_sprites, zombie_group])

	# collisions
	for zombie in zombie_group:
		if pygame.sprite.spritecollide(zombie, bullet_group, True):
			zombie.health -= GUN_DAMAGE

	if pygame.sprite.spritecollideany(player, zombie_group):
		player.health -= 30 * dt
			
	# draw
	all_sprites.customize_draw(player)

	# healthbar and ui
	pygame.draw.rect(display_surface, (100, 30, 30), (50, WINDOW_HEIGHT - 50, WINDOW_WIDTH /3, 35), border_radius = 8)
	if player.health > 0:
		size_n_pos = (50, WINDOW_HEIGHT - 50, WINDOW_WIDTH /3 * (player.health /100), 35)
		pygame.draw.rect(display_surface, (0, 150, 0), size_n_pos, border_radius = 8)

	text_surface = font.render(f"SCORE: {SCORE[0]}", True, "black")
	display_surface.blit(text_surface, (WINDOW_WIDTH /2 - text_surface.get_width() /2, 20))

	text_surface = font.render(f"Wave {wave}", True, "black")
	display_surface.blit(text_surface, (WINDOW_WIDTH /2 - text_surface.get_width() /2, 60))

	# if player is dead
	if player.health <= 0:
		if SCORE[0] > HIGHSCORE:
			HIGHSCORE = SCORE[0]
			highscore_file = open("highscore.txt", "w")
			highscore_file.write(str(HIGHSCORE))

		font = pygame.font.SysFont("", 80)
		display_surface.fill("black")
		text_surface = font.render("You Died", True, "white")
		display_surface.blit(text_surface, (WINDOW_WIDTH /2 - text_surface.get_width() /2, 200))
		text_surface = font.render(f"Score: {SCORE[0]}", True, "white")
		display_surface.blit(text_surface, (WINDOW_WIDTH /2 - text_surface.get_width() /2, 300))
		text_surface = font.render(f"HighScore: {HIGHSCORE}", True, "white")
		display_surface.blit(text_surface, (WINDOW_WIDTH /2 - text_surface.get_width() /2, 400))

		font = pygame.font.SysFont("", 50)
		text_surface = font.render("PRESS ESC TO RESTART", True, "white")
		display_surface.blit(text_surface, (10, WINDOW_HEIGHT - 55))
	else:
		all_sprites.update(dt, player.rect.center, player.rotation)

	pygame.display.update()