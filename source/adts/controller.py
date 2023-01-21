import numpy as np
import pygame


class Controller:
    """Controls the robot"""

    def __init__(
        self, linear_velocity: float, angular_velocity: float, mode: str, frequency: int
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
        self.__n_frames = 0
        self.__timer = None
        self.__frequency = frequency

    def collided(self) -> None:
        """Changes control after colision"""

        if self.__automatic and self.__timer is None:
            # Rotating
            direction = np.random.choice([-1, 1])
            percent = np.random.uniform(1 / 4, 1)

            self.__timer = percent * np.pi / self.__default[1]  # Delta t
            self.__timer *= self.__frequency  # Number of frames
            self.__controls = np.array([0, direction * self.__default[1]])

            self.__n_frames = 0
            self.__motors = False

    def get_controls(self, keys=None) -> np.array:
        """Get current controls"""
        if self.__automatic:
            # Check if timer ended and update controls
            if self.__timer is not None and self.__n_frames > self.__timer:
                # Moving forwar
                self.__controls = np.array([self.__default[0], 0])
                self.__motors = True
                self.__timer = None

            self.__n_frames += 1

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
