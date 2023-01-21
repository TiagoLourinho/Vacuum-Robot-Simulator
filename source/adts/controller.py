import numpy as np
import pygame


class Controller:
    """Controls the robot"""

    def __init__(
        self, linear_velocity: float, angular_velocity: float, mode: str, frequency: int
    ) -> None:
        self.automatic = mode == "automatic"
        self.default = np.array([linear_velocity, angular_velocity])

        if self.automatic:
            self.controls = np.array([linear_velocity, 0])
            self.motors = True
        else:
            self.controls = np.array([0, 0])
            self.motors = False

        # Used for a timer to rotate the robot
        self.n_frames = 0
        self.timer = None
        self.frequency = frequency

    def get_controls(self, keys=None) -> np.array:
        """Get current controls"""

        if self.automatic:
            # Check if timer ended and update controls
            if self.timer is not None and self.n_frames > self.timer:
                # Moving forwar
                self.controls = np.array([self.default[0], 0])
                self.motors = True
                self.timer = None

            self.n_frames += 1
        else:
            if keys[pygame.K_w]:
                self.controls = np.array([self.default[0], 0])
            elif keys[pygame.K_a]:
                self.controls = np.array([0, self.default[1]])
            elif keys[pygame.K_s]:
                self.controls = np.array([-self.default[0], 0])
            elif keys[pygame.K_d]:
                self.controls = np.array([0, -self.default[1]])
            elif keys[pygame.K_RETURN]:
                self.controls = np.array([0, 0])

            self.motors = keys[pygame.K_SPACE]

        return self.controls, self.motors

    def collided(self) -> None:
        """Changes control after colision"""

        if self.automatic and self.timer is None:
            # Rotating
            direction = np.random.choice([-1, 1])
            percent = np.random.uniform(1 / 4, 1)

            self.timer = percent * np.pi / self.default[1]  # Delta t
            self.timer *= self.frequency  # Number of frames
            self.controls = np.array([0, direction * self.default[1]])

            self.n_frames = 0
            self.motors = False
