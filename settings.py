# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0, 155, 155)

# Game options/settings
TITLE = "Flying Duck"
ICON = "icon.png"
SPRITESHEET = "spritesheet.png"
HIGHSCORE = "highscore.txt"
BACKGROUND = "background.png"
FONTNAME = "arial"
WIDTH = 480
HEIGHT = 600
FPS = 60

# Game sounds
SOUND_VOLUME = 0.4
SOUND_FLAP = "flap.wav"
SOUND_POINT = "point.wav"
SOUND_CRASH = "crash.wav"

# Game properties
SCALE = 2
PLAYER_LAYER = 2
OB_LAYER = 1
BACKGROUND_LAYER = 0
BACKGROUND_SPEED = -1
BACKGROUND_COLOR = LIGHT_BLUE

# Player properties
PLAYER_FLAP = 10
PLAYER_GRAVITY = 0.7
PLAYER_ACCELARATION = 0.5

# Obstacle properties
OB_GAP = 50
OB_SPEED = -2
OB_SH = HEIGHT / 2 + 24 + OB_GAP # Start height for bottom obstacle
OB_HEIGHT = 300 * SCALE
OB_TSH = OB_SH - OB_HEIGHT - 2 * OB_GAP - 48 # Start height for top obstacle
OB_LIST = [(WIDTH, OB_SH, False),       (WIDTH, OB_TSH, True),
           (WIDTH + 200, OB_SH, False), (WIDTH + 200, OB_TSH, True), 
           (WIDTH + 400, OB_SH, False), (WIDTH + 400, OB_TSH, True)]