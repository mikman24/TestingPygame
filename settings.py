# Game options/settings
TITLE = "Flying Duck"
ICON = "icon.png"
SPRITESHEET = "spritesheet.png"
WIDTH = 480
HEIGHT = 600
FPS = 60

# Game sounds
SOUND_FLAP = "flap.wav"
SOUND_POINT = "point.wav"
SOUND_CRASH = "crash.wav"

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 155, 155)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = LIGHT_BLUE

# Game properties
SCALE = 2
PLAYER_LAYER = 2
OB_LAYER = 1

# Player properties
PLAYER_FLAP = 10
PLAYER_GRAVITY = 0.7
PLAYER_ACCELARATION = 0.5

# Obstacle properties
OB_GAP = 50
OB_SPEED = 1
OB_SH = HEIGHT / 2 + 24 + OB_GAP
OB_HEIGHT = 300 * SCALE
OB_TSH = OB_SH - OB_HEIGHT - 2 * OB_GAP - 48
OB_LIST = [(WIDTH, OB_SH, False),       (WIDTH, OB_TSH, True),
           (WIDTH + 200, OB_SH, False), (WIDTH + 200, OB_TSH, True), 
           (WIDTH + 400, OB_SH, False), (WIDTH + 400, OB_TSH, True)]