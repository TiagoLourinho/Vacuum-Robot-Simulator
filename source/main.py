import pygame
import os
import numpy as np

from adts import House, VacuumRobot

# Hyperparameters
FREQUENCY = 60  # Hz
N_DUST = 50  # number of dust
WIDTH, HEIGHT = 960, 540  # Pixels
ROBOT_LENGTH = 50  # Pixels
DUST_WIDTH, DUST_HEIGHT = 18, 12  # Pixels

# Initialization
pygame.font.init()
TEXT_FONT = pygame.font.SysFont("comicsans", 40)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vacuum Robot Simulator")

ROBOT_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "robot.png")), (ROBOT_LENGTH, ROBOT_LENGTH)
)
DUST_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "dust.png")), (DUST_WIDTH, DUST_HEIGHT)
)
GREY = (220, 220, 220)
BLACK = (0, 0, 0)
BROWN = (174, 71, 40)


def draw_window(house: House, robot: VacuumRobot):

    x, y, theta = robot.get_state()
    dust = house.get_dust_spots()
    walls = house.get_wall_spots()
    cleaned_text = TEXT_FONT.render(
        f"Cleaned: {round(100*(N_DUST-len(dust))/N_DUST)}%", 1, BLACK
    )

    WIN.fill(GREY)  # Background

    WIN.blit(cleaned_text, (0, 0))  # Cleaned percent text

    # Draw walls
    for w in walls:
        pygame.draw.line(WIN, BROWN, w, w)

    # Draw dust
    for d in dust:
        WIN.blit(DUST_IMAGE, d - np.array([DUST_WIDTH // 2, DUST_HEIGHT // 2]))

    WIN.blit(
        pygame.transform.rotate(ROBOT_IMAGE, np.rad2deg(theta)),
        (round(x) - ROBOT_LENGTH // 2, round(y) - ROBOT_LENGTH // 2),
    )  # Robot

    pygame.display.update()


def main():
    house = House(WIDTH, HEIGHT)
    robot = VacuumRobot(ROBOT_LENGTH / 2)

    # FIXME: Change walls and initial robot position
    y = HEIGHT // 3
    for i in range(WIDTH // 3, 2 * WIDTH // 3):
        house.add_wall(i, y)
        house.add_wall(i, 2 * y)

    x = WIDTH // 3
    for i in range(HEIGHT // 3, 2 * HEIGHT // 3):
        house.add_wall(x, i)
        house.add_wall(2 * x, i)

    robot.set_pose(WIDTH / 2, HEIGHT / 2, 0)

    house.generate_dust(N_DUST, DUST_WIDTH, DUST_HEIGHT)

    clock = pygame.time.Clock()

    while True:
        clock.tick(FREQUENCY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        draw_window(house, robot)


if __name__ == "__main__":
    main()
