import pygame
import os
import numpy as np
import time

from adts import House, VacuumRobot, Controller

# Hyperparameters
FREQUENCY = 60  # Hz
N_DUST = 100  # number of dust
LINEAR_VELOCITY = 500  # Pixel/s
ANGULAR_VELOCITY = 2 * np.pi  # Rad/s
WIDTH, HEIGHT = 960, 540  # Pixels
ROBOT_LENGTH = 50  # Pixels
DUST_WIDTH, DUST_HEIGHT = 18, 12  # Pixels

# Initialization
pygame.init()

TEXT_FONT = pygame.font.SysFont("comicsans", 40)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vacuum Robot Simulator")

ROBOT_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "robot.png")), (ROBOT_LENGTH, ROBOT_LENGTH)
)
DUST_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "dust.png")), (DUST_WIDTH, DUST_HEIGHT)
)
COLLISION_SOUND = pygame.mixer.Sound("assets/collision.wav")
COLLISION_SOUND.set_volume(0.2)

GREY = (220, 220, 220)
BLACK = (0, 0, 0)
BROWN = (174, 71, 40)
BLUE = (65, 105, 225)
LIGHT_BLUE = (171, 219, 227)
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


def setup_game():
    """Draws the house walls"""

    # Wall draw initialization
    WIN.fill(GREY)
    start_button_text = TEXT_FONT.render(f"Start Game", 1, BLACK)
    start_button_rect = start_button_text.get_rect()
    start_button_rect.width += int(0.2 * start_button_text.get_width())
    start_button_rect.height += int(0.2 * start_button_text.get_height())
    pygame.draw.rect(WIN, BLUE, start_button_rect)
    WIN.blit(
        start_button_text,
        (0.1 * start_button_text.get_width(), 0.1 * start_button_text.get_height()),
    )
    pygame.display.update()

    walls = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        left_click = pygame.mouse.get_pressed()[0]

        pos = pygame.mouse.get_pos()

        pygame.draw.rect(
            WIN,
            BLUE if not start_button_rect.collidepoint(pos) else LIGHT_BLUE,
            start_button_rect,
        )
        WIN.blit(
            start_button_text,
            (0.1 * start_button_text.get_width(), 0.1 * start_button_text.get_height()),
        )

        if left_click:

            if not start_button_rect.collidepoint(pos):
                for x in range(5):
                    for y in range(5):
                        cur = (pos[0] + x, pos[1] + y)
                        walls.append(cur)
                        pygame.draw.line(WIN, BROWN, cur, cur)

            # Clicked in start game
            else:
                break
        pygame.display.update()

    # Game mode initialization
    WIN.fill(GREY)

    auto_button_text = TEXT_FONT.render(f"Automatic Control", 1, BLACK)
    auto_button_rect = auto_button_text.get_rect()
    auto_button_rect.width += int(0.2 * auto_button_text.get_width())
    auto_button_rect.height += int(0.2 * auto_button_text.get_height())
    auto_button_rect.move_ip(
        (WIDTH - auto_button_rect.width) // 2, (HEIGHT - auto_button_rect.height) // 2
    )
    pygame.draw.rect(WIN, BLUE, auto_button_rect)
    WIN.blit(
        auto_button_text,
        (
            (WIDTH - auto_button_rect.width) // 2 + 0.1 * auto_button_text.get_width(),
            (HEIGHT - auto_button_rect.height) // 2
            + 0.1 * auto_button_text.get_height(),
        ),
    )

    manual_button_text = TEXT_FONT.render(f"Manual Control", 1, BLACK)
    manual_button_rect = manual_button_text.get_rect()
    manual_button_rect.width += int(0.2 * manual_button_text.get_width())
    manual_button_rect.height += int(0.2 * manual_button_text.get_height())
    manual_button_rect.move_ip(
        (WIDTH - manual_button_rect.width) // 2,
        (HEIGHT - manual_button_rect.height) // 2 + 1.2 * auto_button_rect.height,
    )
    pygame.draw.rect(WIN, BLUE, manual_button_rect)
    WIN.blit(
        manual_button_text,
        (
            (WIDTH - manual_button_rect.width) // 2
            + 0.1 * manual_button_text.get_width(),
            (HEIGHT - manual_button_rect.height) // 2
            + 0.1 * manual_button_text.get_height()
            + 1.2 * auto_button_rect.height,
        ),
    )

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pos = pygame.mouse.get_pos()

        # Automatic control
        if auto_button_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            WIN.fill(GREY)
            text = TEXT_FONT.render(
                "The robot will be automatically controlled",
                1,
                BLACK,
            )
            WIN.blit(
                text,
                ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2),
            )
            pygame.display.update()
            pygame.time.wait(5000)

            return walls, "automatic"

        # Manual control
        if manual_button_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            WIN.fill(GREY)
            text = [
                "Controlling the robot:",
                "W - Move forward",
                "A - Rotate counter-clockwise",
                "S - Move backwards",
                "D - Rotate clockwise",
                "SPACEBAR - Toggle vacuum motors",
            ]

            text = [TEXT_FONT.render(t, 1, BLACK) for t in text]

            offset = 0
            x_offset = text[1].get_width()
            for t in text:
                WIN.blit(
                    t,
                    (
                        (WIDTH - x_offset) // 2,
                        (HEIGHT - t.get_height()) // 2 + offset,
                    ),
                )
                if not offset:
                    offset += 2 * t.get_height()
                else:
                    offset += 1.1 * t.get_height()
            pygame.display.update()
            pygame.time.wait(5000)

            return walls, "manual"

        pygame.draw.rect(
            WIN,
            BLUE if not auto_button_rect.collidepoint(pos) else LIGHT_BLUE,
            auto_button_rect,
        )
        WIN.blit(
            auto_button_text,
            (
                (WIDTH - auto_button_rect.width) // 2
                + 0.1 * auto_button_text.get_width(),
                (HEIGHT - auto_button_rect.height) // 2
                + 0.1 * auto_button_text.get_height(),
            ),
        )
        pygame.draw.rect(
            WIN,
            BLUE if not manual_button_rect.collidepoint(pos) else LIGHT_BLUE,
            manual_button_rect,
        )
        WIN.blit(
            manual_button_text,
            (
                (WIDTH - manual_button_rect.width) // 2
                + 0.1 * manual_button_text.get_width(),
                (HEIGHT - manual_button_rect.height) // 2
                + 0.1 * manual_button_text.get_height()
                + 1.2 * auto_button_rect.height,
            ),
        )
        pygame.display.update()


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
    walls, control = setup_game()
    house = House(WIDTH, HEIGHT, walls)
    robot = VacuumRobot(
        ROBOT_LENGTH // 2, *house.get_charging_station_location(ROBOT_LENGTH)
    )
    controller = Controller(LINEAR_VELOCITY, ANGULAR_VELOCITY)

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
            COLLISION_SOUND.play()
            controller.collided()

        draw_window(house, robot)

    show_final_score(time.time())


if __name__ == "__main__":
    main()
