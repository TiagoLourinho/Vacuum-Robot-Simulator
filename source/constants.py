import pygame
import os
import numpy as np

pygame.init()

##### Hyperparameters #####
FREQUENCY = 30  # Hz
N_DUST = 100  # number of dust
LINEAR_VELOCITY = 200  # Pixel/s
ANGULAR_VELOCITY = np.pi  # Rad/s

##### Default #####
WIDTH, HEIGHT = 960, 540  # Pixels
ROBOT_LENGTH = 50  # Pixels
DUST_WIDTH, DUST_HEIGHT = 18, 12  # Pixels
WALL_SIZE = 3  # Pixels
DEFAULT_WALLS = np.load(os.path.join("assets", "default_walls.npy"))

##### Main screen #####
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vacuum Robot Simulator")

##### Images #####
ROBOT_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "robot.png")), (ROBOT_LENGTH, ROBOT_LENGTH)
)
DUST_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "dust.png")), (DUST_WIDTH, DUST_HEIGHT)
)

##### Sounds #####
COLLISION_SOUND = pygame.mixer.Sound(os.path.join("assets", "collision.wav"))
COLLISION_SOUND.set_volume(0.1)
VACUUM_SOUND = pygame.mixer.Sound(os.path.join("assets", "vacuum.wav"))
VACUUM_SOUND.set_volume(0.05)

##### Text Fonts #####
TEXT_FONT = pygame.font.SysFont("comicsans", 40)

##### Colors #####
GREY = (220, 220, 220)
BLACK = (0, 0, 0)
BROWN = (174, 71, 40)
BLUE = (65, 105, 225)
LIGHT_BLUE = (171, 219, 227)
PY_GREEN = (170, 238, 187)
