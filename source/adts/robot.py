import numpy as np


class VacuumRobot:
    def __init__(
        self, radius: float, x: float = 0, y: float = 0, theta: float = 0
    ) -> None:

        self.__radius = radius
        self.__state = np.array([x, y, theta])

    def move(self, control: np.array, t_step: float) -> None:
        """Moves the robot and returns new pose"""

        A = np.array(
            [
                [t_step * np.cos(self.__state[2]), 0],
                [t_step * np.sin(self.__state[2]), 0],
                [0, t_step],
            ]
        )
        self.__state += A @ control

    def get_state(self) -> np.array:
        """Returns the current state"""

        return self.__state

    def set_pose(self, x: float, y: float, theta: float) -> None:
        """Puts the robot in the defined position"""

        self.__state = np.array([x, y, theta])
