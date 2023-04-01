import pygame
from settings import *

class Game:
    def __init__(self):
        # Initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.icon = pygame.display.set_icon()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        pass

    def update(self):
        pass

g = Game()
while g.running:
    g.new()

pygame.quit()