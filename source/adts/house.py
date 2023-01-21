import numpy as np


class House:
    """Represents a house with dust"""

    def __init__(self, width: int, height: int, walls: np.array) -> None:
        self.width = width
        self.heigth = height
        self.walls = np.full((height, width), False)
        self.dust = np.full((height, width), False)

        for w in walls:
            self.walls[w[1], w[0]] = True

        (
            self.min_x,
            self.max_x,
            self.min_y,
            self.max_y,
        ) = self.get_surrounding_rectangle()

    def get_free_spot(self) -> tuple:
        """Returns a free spot on the map"""

        while True:
            x = np.random.randint(self.min_x + 1, self.max_x)
            y = np.random.randint(self.min_y + 1, self.max_y)

            # Generate a spot for robot without walls, dust and inside the house
            if (
                not self.walls[y, x]
                and not self.dust[y, x]
                and self.is_inside_house(x, y)
            ):

                return (x, y)

    def dirty(self, x: int, y: int) -> None:
        """Puts dust in that spot"""

        self.dust[y, x] = True

    def clean(self, x: int, y: int) -> None:
        """Cleans the dust from that spot"""

        self.dust[y, x] = False

    def is_inside_house(self, x: int, y: int) -> bool:
        """Checks if a point (`x`, `y`) is inside the house"""

        collisions = 0

        if self.walls[y, x]:
            return False

        # Left border
        for i in range(x, -1, -1):
            if self.walls[y, i]:
                collisions += 1
                break

        # Right border
        for i in range(x, self.width):
            if self.walls[y, i]:
                collisions += 1
                break

        # Upper border
        for i in range(y, -1, -1):
            if self.walls[i, x]:
                collisions += 1
                break

        # Lower border
        for i in range(y, self.heigth):
            if self.walls[i, x]:
                collisions += 1
                break

        if collisions == 4:
            return True
        else:
            return False

    def get_surrounding_rectangle(self) -> tuple[int]:
        """Returns the coordinates of a rectangle that envolves all the walls"""

        min_x = 0
        max_x = self.width
        min_y = 0
        max_y = self.heigth

        # Left border
        for i in range(0, self.width):
            if np.any(self.walls[:, i]):
                min_x = i
                break

        # Right border
        for i in range(self.width - 1, -1, -1):
            if np.any(self.walls[:, i]):
                max_x = i
                break

        # Upper border
        for i in range(0, self.heigth):
            if np.any(self.walls[i, :]):
                min_y = i
                break

        # Lower border
        for i in range(self.heigth - 1, -1, -1):
            if np.any(self.walls[i, :]):
                max_y = i
                break

        return min_x, max_x, min_y, max_y
