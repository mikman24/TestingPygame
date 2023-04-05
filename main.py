# Testing out pygame by making a clone of the famous Flappy Bird game.
import pygame, os, random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # Initialize game
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.homeDir = os.getcwd()
        self.imgDir = os.path.join(self.homeDir, "img")
        self.sndDir = os.path.join(self.homeDir, "snd")
        self.icon = pygame.image.load(os.path.join(self.imgDir, ICON)).convert()
        self.icon.set_colorkey(BLACK)
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.loadAssets()

    def new(self):
        # Start new game
        self.allSprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.player = Player(self)
        self.allSprites.add(self.player)
        self.obstacleBottom = Obstacle(self, 40, 300, False)
        self.obstacles.add(self.obstacleBottom)
        self.obstacleTop = Obstacle(self, WIDTH-100, -300, True)
        self.obstacles.add(self.obstacleTop)
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Update game loop
        self.allSprites.update()
        self.obstacles.update()
        # Game over if player hits top or bottom of screen
        if self.player.rect.bottom >= HEIGHT or self.player.rect.top <= 0:
            self.player.gotHit()

    def events(self):
        # Process player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.player.flap()

    def draw(self):
        # Update all drawings
        self.screen.fill(BACKGROUND_COLOR)
        self.allSprites.draw(self.screen)
        pygame.display.flip()

    def loadAssets(self):
        # Load spritesheet
        self.spritesheet = Spritesheet(os.path.join(self.imgDir, SPRITESHEET))
        # Load sounds
        self.flapSound = pygame.mixer.Sound(os.path.join(self.sndDir, SOUND_FLAP))
        self.pointSound = pygame.mixer.Sound(os.path.join(self.sndDir, SOUND_POINT))
        self.crashSound = pygame.mixer.Sound(os.path.join(self.sndDir, SOUND_CRASH))

g = Game()
while g.running:
    g.new()

pygame.quit()