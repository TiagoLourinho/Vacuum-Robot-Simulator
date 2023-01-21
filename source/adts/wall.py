import pygame
import numpy as np


class Wall(pygame.sprite.Sprite):
    """Represents a wall spot"""

    def __init__(self, color: tuple, x: int, y: int) -> None:
        super().__init__()
        self.pos = np.array([x, y])
        self.image = pygame.Surface((1, 1))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
