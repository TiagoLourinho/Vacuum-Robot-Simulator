import numpy as np
import time
import pygame


class Controller:
    """Controls the robot"""

    def __init__(
        self, linear_velocity: float, angular_velocity: float, mode: str
    ) -> None:
        self.__automatic = mode == "automatic"
        self.__default = np.array([linear_velocity, angular_velocity])

        if self.__automatic:
            self.__controls = np.array([linear_velocity, 0])
            self.__motors = True
        else:
            self.__controls = np.array([0, 0])
            self.__motors = False

        # Used for a timer to rotate the robot
        self.__rotating_start = None
        self.__timer = None

    def collided(self) -> None:
        """Changes control after colision"""

        if self.__automatic and self.__timer is None:
            # Rotating
            self.__timer = (
                np.random.uniform(1 / 4, 3 / 4) * 2 * np.pi / self.__default[1]
            )
            self.__controls = np.array([0, self.__default[1]])
            self.__rotating_start = time.time()
            self.__motors = False

    def get_controls(self, keys=None) -> np.array:
        """Get current controls"""
        if self.__automatic:
            # Check if timer ended and update controls
            if (
                self.__timer is not None
                and time.time() - self.__rotating_start > self.__timer
            ):
                # Moving forwar
                self.__controls = np.array([self.__default[0], 0])
                self.__motors = True
                self.__timer = None

        else:
            if keys[pygame.K_w]:
                self.__controls = np.array([self.__default[0], 0])
            elif keys[pygame.K_a]:
                self.__controls = np.array([0, self.__default[1]])
            elif keys[pygame.K_s]:
                self.__controls = np.array([-self.__default[0], 0])
            elif keys[pygame.K_d]:
                self.__controls = np.array([0, -self.__default[1]])
            elif keys[pygame.K_LSHIFT]:
                self.__controls = np.array([0, 0])

            self.__motors = keys[pygame.K_SPACE]

        return self.__controls, self.__motors
