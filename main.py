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
        self.allSprites = pygame.sprite.LayeredUpdates()
        self.obstacles = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.player = Player(self)
        for o in OB_LIST:
            Obstacle(self, *o)
        Background(self, 0)
        Background(self, WIDTH)
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
        # Game over if player hits top or bottom of screen
        # obstacleHits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
        obstacleHits = False
        if obstacleHits or self.player.rect.bottom >= HEIGHT or self.player.rect.top <= 0:
            self.player.gotHit()
        # If Obstacles reach left of the screen
        for o in self.obstacles:
            if o.rect.right <= 0:
                o.kill()
        # Spawn new obstacles to keep the same average number
        totalGap = OB_GAP * 2 + self.player.image.get_height()
        while len(self.obstacles) < 6:
            bottomHeight = random.randrange(92 + totalGap, HEIGHT - 92)
            Obstacle(self, WIDTH + 40, bottomHeight, False)
            topHeight = bottomHeight - totalGap - OB_HEIGHT
            Obstacle(self, WIDTH + 40, topHeight, True)
        # Scroll background
        for b in self.backgrounds:
            if b.rect.right <= 0:
                b.kill()
                print("killed background")
        while len(self.backgrounds) < 2:
            Background(self, WIDTH)

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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.flappingFrame(False)

    def draw(self):
        # Update all drawings
        self.screen.fill(BACKGROUND_COLOR)
        self.allSprites.draw(self.screen)
        pygame.display.flip()

    def loadAssets(self):
        # Load images
        self.spritesheet = Spritesheet(os.path.join(self.imgDir, SPRITESHEET))
        self.background = pygame.image.load(os.path.join(self.imgDir, BACKGROUND)).convert()
        # Load sounds
        self.flapSound = pygame.mixer.Sound(os.path.join(self.sndDir, SOUND_FLAP))
        self.pointSound = pygame.mixer.Sound(os.path.join(self.sndDir, SOUND_POINT))
        self.crashSound = pygame.mixer.Sound(os.path.join(self.sndDir, SOUND_CRASH))

g = Game()
while g.running:
    g.new()

pygame.quit()