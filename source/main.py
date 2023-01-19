import pygame
import os
import numpy as np
import time

from adts import House, VacuumRobot, Controller

# Hyperparameters
FREQUENCY = 60  # Hz
N_DUST = 100  # number of dust
LINEAR_VELOCITY = 100  # Pixel/s
ANGULAR_VELOCITY = np.pi / 4  # Rad/s
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
START_TIME = time.time()


def draw_window(house: House, robot: VacuumRobot):

    x, y, theta = robot.get_state()
    dust = house.get_dust_spots()
    walls = house.get_wall_spots()
    cleaned_text = TEXT_FONT.render(
        f"Cleaned: {int(100*(N_DUST-len(dust))/N_DUST)}%", 1, BLACK
    )
    seconds = round(time.time() - START_TIME)
    time_text = TEXT_FONT.render(f"Time: {seconds//60}min{seconds%60}s", 1, BLACK)

    WIN.fill(GREY)  # Background

    WIN.blit(cleaned_text, (0, 0))  # Cleaned percent text
    WIN.blit(time_text, (0, cleaned_text.get_height()))  # Cleaned time text

    # Draw walls
    for w in walls:
        pygame.draw.line(WIN, BROWN, w, w)

    # Draw dust
    for d in dust:
        WIN.blit(DUST_IMAGE, d - np.array([DUST_WIDTH // 2, DUST_HEIGHT // 2]))

    rotate_and_blit(
        WIN,
        ROBOT_IMAGE,
        (round(x), round(y)),
        (ROBOT_LENGTH // 2, ROBOT_LENGTH // 2),
        np.rad2deg(theta),
    )  # Robot

    pygame.display.update()


def rotate_and_blit(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
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


def show_final_score(final_time):
    message_text = TEXT_FONT.render(f"All cleaned!", 1, BLACK)
    seconds = round(final_time - START_TIME)
    time_text = TEXT_FONT.render(f"Time: {seconds//60}min{seconds%60}s", 1, BLACK)

    WIN.fill(GREY)  # Background

    WIN.blit(
        message_text,
        (
            (WIDTH - message_text.get_width()) // 2,
            (HEIGHT - message_text.get_height()) // 2,
        ),
    )  # Cleaned percent text
    WIN.blit(
        time_text,
        (
            (WIDTH - time_text.get_width()) // 2,
            (HEIGHT - time_text.get_height()) // 2 + message_text.get_height(),
        ),
    )  # Cleaned time text

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def main():
    house = House(WIDTH, HEIGHT)
    robot = VacuumRobot(ROBOT_LENGTH // 2)
    controller = Controller(LINEAR_VELOCITY, ANGULAR_VELOCITY)

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

        # All cleaned
        if int(100 * (N_DUST - len(house.get_dust_spots())) / N_DUST) == 100:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        robot.move(controller.get_controls(), 1 / FREQUENCY)

        # Vacuum
        for vacuumed in robot.vacuum(house.get_dust_spots()):
            house.clean(*vacuumed)

        # Hit wall
        if robot.hits_wall(house.get_wall_spots()):

            controller.collided()

        draw_window(house, robot)

    show_final_score(time.time())


if __name__ == "__main__":
    main()
