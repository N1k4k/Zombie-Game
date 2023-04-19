import pygame, sys
from settings import *

pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('2D fighting game')


class Button():
	def __init__(self, pos, size, text, fontsize):
		self.pos = pos
		self.size = size
		self.text = text

		self.font = pygame.font.SysFont("", fontsize)

		self.text_surface = self.font.render(text, True, (255, 255, 255))

		text_size = self.text_surface.get_size()
		self.text_pos = self.pos[0] + self.size[0] /2 - text_size[0] /2, self.pos[1] + self.size[1] /2 - text_size[1] /2

	def draw(self):
		rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
		pygame.draw.rect(display_surface, (0, 50, 30), rect, border_radius = 10)
		display_surface.blit(self.text_surface, self.text_pos)

	def isClicked(self, mouse_pos):
		if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1]:
			return 1


buttons = [
	Button((350, 230), (350, 90), "Start", 50),
	Button((350, 350), (350, 90), "Instructions", 50),
	Button((350, 470), (350, 90), "Exit", 50),
]

font = pygame.font.SysFont("", 70)
menu_type = "menu"
running = True

back_btn = Button((30, WINDOW_HEIGHT - 120), (350, 90), "Back", 50)

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	display_surface.fill((0, 10, 0))
	font = pygame.font.SysFont("", 70)

	if menu_type == "menu":
		text_surface = font.render("Zombie Survival", True, "green")
		display_surface.blit(text_surface, (WINDOW_WIDTH /2 - text_surface.get_width() /2, 100))

		for btn in buttons:
			btn.draw()
			if pygame.mouse.get_pressed()[0] and btn.isClicked(pygame.mouse.get_pos()):
				if btn.text == "Start":
					running = False
				elif btn.text == "Exit":
					pygame.quit()
					sys.exit()
				elif btn.text == "Instructions":
					menu_type = "instructions"

	elif menu_type == "instructions":
		font = pygame.font.SysFont("", 70)
		text_surface = font.render("Instructions", True, "white")
		display_surface.blit(text_surface, (WINDOW_WIDTH /2 - text_surface.get_width() /2, 100))

		font = pygame.font.SysFont("", 55)
		text_surface = font.render("Press W, A, S, D to move", True, "white")
		display_surface.blit(text_surface, (WINDOW_WIDTH /2 - text_surface.get_width() /2, 170))

		text_surface = font.render("Right click to shoot", True, "white")
		display_surface.blit(text_surface, (WINDOW_WIDTH /2 - text_surface.get_width() /2, 240))

		text_surface = font.render("Survive the zombies as long as you can", True, "white")
		display_surface.blit(text_surface, (WINDOW_WIDTH /2 - text_surface.get_width() /2, 310))

		back_btn.draw()
		if pygame.mouse.get_pressed()[0] and back_btn.isClicked(pygame.mouse.get_pos()):
			menu_type = "menu"


	pygame.display.update()