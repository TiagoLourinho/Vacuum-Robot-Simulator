import numpy as np


class VacuumRobot:
    """Represents a vacuum robot cleaner"""

    def __init__(
        self, radius: float, x: float = 0, y: float = 0, theta: float = 0
    ) -> None:

        self.__radius = radius
        self.__state = np.array([x, y, theta])
        self.__previous_state = np.array([x, y, theta])

    def move(self, control: np.array, t_step: float) -> None:
        """Moves the robot and returns new pose"""

        A = np.array(
            [
                [t_step * np.cos(self.__state[2]), 0],
                [-t_step * np.sin(self.__state[2]), 0],
                [0, t_step],
            ]
        )
        self.__previous_state = self.__state
        self.__state = self.__previous_state + A @ control

    def get_state(self) -> np.array:
        """Returns the current state"""

        return self.__state

    def hits_wall(self, wall) -> bool:
        """Checks if the robot its a wall"""

        # FIXME: Not very efficient because checks every wall spot...

        for w in wall:
            if np.linalg.norm(self.__state[:2] - w) < self.__radius:

                # Didn't move due to a collision

                self.__state = self.__previous_state
                return True

        return False

    def vacuum(self, dust) -> list:
        """Vacuums the dust that are within reach"""

        vacuumed = []

        for d in dust:
            if np.linalg.norm(self.__state[:2] - d) < self.__radius:
                vacuumed.append(d)

        return vacuumed
