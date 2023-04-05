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
        self.image = self.game.spritesheet.getImage(0, 0, 32, 24)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.flapping = False
        self.gameover = False

    def update(self):
        if self.gameover and self.rect.bottom >= HEIGHT:
            self.rect.center = (WIDTH/2, HEIGHT-self.image.get_height()/2)
        else:
            self.fallDown()
       
    def fallDown(self):
        self.acc = vec(0, PLAYER_GRAVITY)        
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.center = self.pos

    def flap(self):
        if not self.gameover:
            self.flapping = True
            self.vel.y = -PLAYER_FLAP

    def gotHit(self):
        self.gameover = True

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, isTop):
        self._layer = OBSTACLE_LAYER
        self.groups = game.allSprites, game.obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.getImage(32, 0, 40, 300)
        self.image.set_colorkey(BLACK)
        if isTop:
            self.image = pygame.transform.flip(self.image, True, True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass