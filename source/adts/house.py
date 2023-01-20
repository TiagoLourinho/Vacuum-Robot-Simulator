import numpy as np


class House:
    """Represents a house with dust"""

    def __init__(self, width: int, height: int, walls: list[tuple[int]]) -> None:
        self.__width = width
        self.__heigth = height
        self.__wall = np.full((height, width), False)
        self.__dust = np.full((height, width), False)

        for w in walls:
            self.__wall[w[1], w[0]] = True

    def get_wall_spots(self) -> np.array:
        """Returns the spots where there is a wall"""

        return list(zip(*np.flip(np.nonzero(self.__wall), axis=0)))

    def get_dust_spots(self) -> np.array:
        """Returns the spots where there is dust"""

        return list(zip(*np.flip(np.nonzero(self.__dust), axis=0)))

    def generate_dust(self, N: int, dust_width: int, dust_height: int) -> None:
        """Generates `N` dust inside the house"""

        min_x, max_x, min_y, max_y = self.get_surrounding_rectangle(
            dust_width // 2, dust_height // 2
        )

        for _ in range(N):
            while True:
                x = np.random.randint(min_x + 1, max_x)
                y = np.random.randint(min_y + 1, max_y)

                # Generate a spot for dust without walls, dust and inside the house
                if (
                    not self.__wall[y, x]
                    and not self.__dust[y, x]
                    and self.is_inside_house(x, y)
                ):

                    self.__dust[y, x] = True
                    break

    def clean(self, x: int, y: int) -> None:
        """Cleans the dust from that spot"""

        self.__dust[y, x] = False

    def is_inside_house(self, x: int, y: int) -> bool:
        """Checks if a point (`x`, `y`) is inside the house"""

        collisions = 0

        # Left border
        for i in range(x, -1, -1):
            if self.__wall[y, i]:
                collisions += 1
                break

        # Right border
        for i in range(x, self.__width):
            if self.__wall[y, i]:
                collisions += 1
                break

        # Upper border
        for i in range(y, -1, -1):
            if self.__wall[i, x]:
                collisions += 1
                break

        # Lower border
        for i in range(y, self.__heigth):
            if self.__wall[i, x]:
                collisions += 1
                break

        if collisions == 4:
            return True
        else:
            return False

    def get_surrounding_rectangle(self, x_offset: int, y_offset: int) -> tuple[int]:
        """Returns the coordinates of a rectangle that envolves all the walls"""

        min_x = 0
        max_x = self.__width
        min_y = 0
        max_y = self.__heigth

        # Left border
        for i in range(0, self.__width):
            if np.any(self.__wall[:, i]):
                min_x = i
                break

        # Right border
        for i in range(self.__width - 1, -1, -1):
            if np.any(self.__wall[:, i]):
                max_x = i
                break

        # Upper border
        for i in range(0, self.__heigth):
            if np.any(self.__wall[i, :]):
                min_y = i
                break

        # Lower border
        for i in range(self.__heigth - 1, -1, -1):
            if np.any(self.__wall[i, :]):
                max_y = i
                break

        return (
            min(min_x + x_offset, max_x - x_offset),
            max(max_x - x_offset, min_x + x_offset),
            min(min_y + y_offset, max_y - y_offset),
            max(max_y - y_offset, min_y + y_offset),
        )

    def get_charging_station_location(self, offset) -> tuple:
        """Returns the initial position for the robot"""

        min_x, max_x, min_y, max_y = self.get_surrounding_rectangle(offset, offset)
        while True:
            x = np.random.randint(min_x + 1, max_x)
            y = np.random.randint(min_y + 1, max_y)

            # Generate a spot for robot without walls, dust and inside the house
            if (
                not self.__wall[y, x]
                and not self.__dust[y, x]
                and self.is_inside_house(x, y)
            ):

                return (x, y)
