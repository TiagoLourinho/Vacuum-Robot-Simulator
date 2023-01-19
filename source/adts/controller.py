import numpy as np
import time


class Controller:
    """Controls the robot"""

    def __init__(self, linear_velocity: float, angular_velocity: float) -> None:
        self.__default = np.array([linear_velocity, angular_velocity])
        self.__controls = np.array([linear_velocity, 0])

        # Used for a timer to rotate the robot
        self.__rotating_start = None
        self.__timer = None

    def collided(self) -> None:
        """Changes control after colision"""
        if self.__timer is None:

            self.__timer = (
                min(max(np.random.rand(), 1 / 4), 3 / 4) * 2 * np.pi / self.__default[1]
            )
            self.__controls = np.array([0, self.__default[1]])
            self.__rotating_start = time.time()

    def get_controls(self) -> np.array:
        """Get current controls"""

        # Check if timer ended and update controls
        if (
            self.__timer is not None
            and time.time() - self.__rotating_start > self.__timer
        ):

            self.__controls = np.array([self.__default[0], 0])
            self.__timer = None

        return self.__controls
