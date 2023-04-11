# Sprite classes for Flappy bird clone
import pygame, random
from settings import *
vec = pygame.math.Vector2

class Spritesheet:
    # Utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def getImage(self, x, y, width, height):
        # Grab an image out of a larger spreadsheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pygame.transform.scale(image, (width*SCALE, height*SCALE))
        return image
    
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.allSprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.loadImages()
        self.image = self.downFrame
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.gameover = False

    def loadImages(self):
        self.downFrame = self.game.spritesheet.getImage(0, 0, 32, 24)
        self.downFrame.set_colorkey(BLACK)
        self.flapFrame = self.game.spritesheet.getImage(0, 24, 32, 24)
        self.flapFrame.set_colorkey(BLACK)

    def flappingFrame(self, flap):
        if flap:
            self.image = self.flapFrame
        else:
            self.image = self.downFrame

    def update(self):
        if self.gameover and self.rect.bottom >= HEIGHT:
            self.rect.center = (WIDTH / 2 , HEIGHT - self.image.get_height() / 2)
            self.game.playing = False
        else:
            self.fallDown()
       
    def fallDown(self):
        self.acc = vec(0, PLAYER_GRAVITY)        
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

    def flap(self):
        if not self.gameover:
            self.game.flapSound.play()
            self.flappingFrame(True)
            self.vel.y = -PLAYER_FLAP

    def gotHit(self):
        self.gameover = True

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, isTop):
        self._layer = OB_LAYER
        self.groups = game.allSprites, game.obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.top = isTop
        self.image = self.game.spritesheet.getImage(32, 0, 40, 300)
        self.image.set_colorkey(BLACK)
        if self.top:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gotPoint = False
        self.obstacleSpeed = OB_SPEED

    def addPoint(self):
        self.gotPoint = True

    def update(self):
        self.rect.x += self.obstacleSpeed

class Background(pygame.sprite.Sprite):
    def __init__(self, game, x):
        self._layer = BACKGROUND_LAYER
        self.groups = game.allSprites, game.backgrounds
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.background
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.backgroundSpeed = BACKGROUND_SPEED

    def update(self):
        self.rect.x += self.backgroundSpeed