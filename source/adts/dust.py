import pygame
import numpy as np


class Dust(pygame.sprite.Sprite):
    """Represents a dust spot"""

    def __init__(self, image: pygame.Surface, x: int, y: int) -> None:
        super().__init__()
        self.pos = np.array([x, y])
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = self.pos

    def draw(self, surface: pygame.Surface):
        """Blits the dust to the screen"""

        surface.blit(self.image, self.rect)

    def get_pos(self) -> np.array:
        """Getter for position"""

        return self.pos
