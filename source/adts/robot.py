import numpy as np
import pygame


class VacuumRobot(pygame.sprite.Sprite):
    """Represents a vacuum robot cleaner"""

    def __init__(
        self,
        image: pygame.Surface,
        radius: float,
        x: float = 0,
        y: float = 0,
        theta: float = 0,
    ) -> None:
        super().__init__()
        # Robot state
        self.radius = radius
        self.state = np.array([x, y, theta])
        self.previous_state = np.array([x, y, theta])

        # Pygame
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = (x, y)

    def move(self, control: np.array, t_step: float) -> None:
        """Moves the robot"""

        A = np.array(
            [
                [t_step * np.cos(self.state[2]), 0],
                [-t_step * np.sin(self.state[2]), 0],
                [0, t_step],
            ]
        )
        self.previous_state = self.state
        self.state = self.previous_state + A @ control

        self.rect.center = self.state[:2]

    def collided(self) -> None:
        """Returns to the previous state"""

        self.state = self.previous_state
        self.rect.center = self.state[:2]

    def draw(self, surface: pygame.Surface):
        """Blits the robot to the screen"""

        self.rotate_and_blit(
            surface,
            self.image,
            (round(self.state[0]), round(self.state[1])),
            (self.radius, self.radius),
            np.rad2deg(self.state[2]),
        )  # Robot

    def rotate_and_blit(self, surf, image, pos, originPos, angle):
        """Helper function so a rotated image keeps dimensions"""

        # offset from pivot to center
        image_rect = image.get_rect(
            topleft=(pos[0] - originPos[0], pos[1] - originPos[1])
        )
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

        # rotated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # rotated image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        # rotate and blit the image
        surf.blit(rotated_image, rotated_image_rect)

    def get_rect(self) -> pygame.Rect:
        """Getter for the rectangle"""

        return self.rect

    def get_radius(self) -> float:
        """Getter for the radius"""

        return self.radius

    def get_state(self) -> np.array:
        """Getter for the state"""

        return self.state.copy()
