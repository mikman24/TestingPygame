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
        self.fontName = pygame.font.match_font(FONTNAME)
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
        self.score = 0
        self.hitSound = False
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
        obstacleHits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
        if obstacleHits or self.player.rect.bottom >= HEIGHT or self.player.rect.top <= 0:
            if not self.hitSound:
                self.hitSound = True
                self.crashSound.play()
            self.gameOver()
        # Add point for every top obstacle or kill obstacles
        for o in self.obstacles:
            if o.rect.right <= WIDTH / 2 and not o.gotPoint and o.top:
                self.pointSound.play()
                o.addPoint()
                self.score += 1
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
        while len(self.backgrounds) < 2:
            Background(self, WIDTH)

    def gameOver(self):
        self.player.gotHit()
        for b in self.backgrounds:
            b.backgroundSpeed = 0
        for o in self.obstacles:
            o.obstacleSpeed = 0

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
        self.drawText(str(self.score), 50, BLACK, WIDTH / 2, 10)
        pygame.display.flip()

    def drawText(self, text, size, color, x, y):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (x, y)
        self.screen.blit(textSurface, textRect)

    def showGameOverScreen(self):
        if not self.running:
            return
        self.screen.fill(BACKGROUND_COLOR)
        self.allSprites.draw(self.screen)
        self.drawText("GAME OVER", 50, BLACK, WIDTH/2, HEIGHT/4)
        self.drawText("Score: " + str(self.score), 48, BLACK,  WIDTH/2, HEIGHT/2)
        self.drawText("Press SPACE to play again", 22, BLACK, WIDTH/2, HEIGHT*3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.drawText("New highscore!", 22, GREEN, WIDTH/2, HEIGHT*3/8)
            with open(os.path.join(self.homeDir, HIGHSCORE), "w") as f:
                f.write(str(self.score))
        else:
            self.drawText("Highscore: " + str(self.highscore), 22, BLACK, WIDTH/2, HEIGHT*3/8)
        pygame.display.flip()
        self.waitForKey()

    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        waiting = False
            

    def loadAssets(self):
        # Highscore file
        with open(HIGHSCORE, "r") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # Load images
        self.spritesheet = Spritesheet(os.path.join(self.imgDir, SPRITESHEET))
        self.background = pygame.image.load(os.path.join(self.imgDir, BACKGROUND)).convert()
        # Load sounds
        self.flapSound = pygame.mixer.Sound(os.path.join(self.sndDir, SOUND_FLAP))
        self.pointSound = pygame.mixer.Sound(os.path.join(self.sndDir, SOUND_POINT))
        self.crashSound = pygame.mixer.Sound(os.path.join(self.sndDir, SOUND_CRASH))
        self.flapSound.set_volume(SOUND_VOLUME)
        self.pointSound.set_volume(SOUND_VOLUME)
        self.crashSound.set_volume(SOUND_VOLUME)

g = Game()
while g.running:
    g.new()
    g.showGameOverScreen()

pygame.quit()