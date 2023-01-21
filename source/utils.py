import pygame
import time

from constants import *
from adts import House, VacuumRobot, Button


def show_loading_screen():
    """Show loading screen"""
    font = pygame.font.SysFont("comicsans", 70, bold=True)
    text = font.render("Vacuum Robot Simulator", 1, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 3)

    image = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "robot.png")),
        (text.get_width() // 3, text.get_width() // 3),
    )
    image_rect = image.get_rect()
    image_rect.center = (WIDTH // 2, 2 * HEIGHT // 3)

    SCREEN.fill((170, 238, 187))
    SCREEN.blit(text, text_rect)
    SCREEN.blit(image, image_rect)

    pygame.display.update()
    pygame.time.delay(2000)


def choose_game_mode():
    """Chooses the game mode to play"""

    SCREEN.fill(GREY)

    automatic_button = Button(
        TEXT_FONT,
        "Automatic Control",
        BLACK,
        BLUE,
        LIGHT_BLUE,
    )
    automatic_button.set_top_left_corner(
        (WIDTH - automatic_button.get_width()) // 2,
        (HEIGHT - automatic_button.get_height()) // 2,
    )

    manual_button = Button(
        TEXT_FONT,
        "Manual Control",
        BLACK,
        BLUE,
        LIGHT_BLUE,
    )
    manual_button.set_top_left_corner(
        (WIDTH - manual_button.get_width()) // 2,
        (HEIGHT - manual_button.get_height()) // 2
        + 1.2 * automatic_button.get_height(),
    )

    SCREEN.blit(
        TEXT_FONT.render(
            "Choose how to control the robot",
            1,
            BLACK,
        ),
        (5, 5),
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]

        # Automatic control
        if left_click:
            if pos in automatic_button:
                SCREEN.fill(GREY)
                text = TEXT_FONT.render(
                    "The robot will be automatically controlled",
                    1,
                    BLACK,
                )
                SCREEN.blit(
                    text,
                    (
                        (WIDTH - text.get_width()) // 2,
                        (HEIGHT - text.get_height()) // 2,
                    ),
                )

                SCREEN.blit(
                    TEXT_FONT.render(
                        "Click anywhere to continue",
                        1,
                        BLACK,
                    ),
                    (0, 0),
                )
                pygame.display.update()
                pygame.time.delay(200)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                    left_click = pygame.mouse.get_pressed()[0]
                    if left_click:
                        pygame.time.delay(100)
                        return "automatic"

            elif pos in manual_button:
                SCREEN.fill(GREY)
                text = [
                    "Controlling the robot:",
                    "W - Move forward",
                    "A - Rotate counter-clockwise",
                    "S - Move backwards",
                    "D - Rotate clockwise",
                    "Space bar - Turn on vacuum",
                    "Enter - Stop robot",
                ]

                text = [TEXT_FONT.render(t, 1, BLACK) for t in text]

                offset = 0
                x_offset = text[0].get_width()
                for t in text:
                    SCREEN.blit(
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

                SCREEN.blit(
                    TEXT_FONT.render(
                        "Click anywhere to continue",
                        1,
                        BLACK,
                    ),
                    (0, 0),
                )
                pygame.display.update()
                pygame.time.delay(200)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                    left_click = pygame.mouse.get_pressed()[0]
                    if left_click:
                        pygame.time.delay(100)
                        return "manual"

        automatic_button.draw(SCREEN, pos)
        manual_button.draw(SCREEN, pos)
        pygame.display.update()


def draw_walls():
    """Initializes the walls"""

    SCREEN.fill(GREY)
    start_button = Button(TEXT_FONT, "Start Game", BLACK, BLUE, LIGHT_BLUE, (5, 5))

    instruction_text = TEXT_FONT.render(
        "Draw the house walls (or don't, to use the default)", 1, BLACK
    )
    SCREEN.blit(
        instruction_text,
        (
            1.2 * start_button.get_width(),
            5 + start_button.get_text_height() * start_button.get_border() / 2,
        ),
    )

    walls = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        left_click = pygame.mouse.get_pressed()[0]
        pos = pygame.mouse.get_pos()

        if left_click:

            # Start game
            if pos in start_button:
                return walls

            # Draw wall
            else:
                for x in range(-WALL_WIDTH // 2, WALL_WIDTH // 2 + 1):
                    for y in range(-WALL_WIDTH // 2, WALL_WIDTH // 2 + 1):
                        cur = (min(pos[0] + x, WIDTH - 1), min(pos[1] + y, HEIGHT - 1))
                        walls.append(cur)
                        pygame.draw.line(SCREEN, BROWN, cur, cur)

        start_button.draw(SCREEN, pos)
        pygame.display.update()


def init_screen(house: House, robot: VacuumRobot) -> None:
    """Initializes the screen"""

    x, y, theta = robot.get_state()
    dust = house.get_dust_spots()
    walls = house.get_wall_spots()

    SCREEN.fill(GREY)

    # Draw walls
    for w in walls:
        pygame.draw.line(SCREEN, BROWN, w, w)

    pygame.time.delay(100)
    pygame.display.update()

    # Draw dust
    for d in dust:
        SCREEN.blit(DUST_IMAGE, d - np.array([DUST_WIDTH // 2, DUST_HEIGHT // 2]))
        pygame.display.update()
        pygame.time.delay(10)

    rotate_and_blit(
        SCREEN,
        ROBOT_IMAGE,
        (round(x), round(y)),
        (ROBOT_LENGTH // 2, ROBOT_LENGTH // 2),
        np.rad2deg(theta),
    )  # Robot

    pygame.time.delay(500)
    pygame.display.update()


def draw_screen(house: House, robot: VacuumRobot, start_time: float) -> None:
    """Draws the general game screen"""

    x, y, theta = robot.get_state()
    dust = house.get_dust_spots()
    walls = house.get_wall_spots()

    # Text
    cleaned_text = TEXT_FONT.render(
        f"Cleaned: {int(100*(N_DUST-len(dust))/N_DUST)}%", 1, BLACK
    )
    seconds = round(time.time() - start_time)
    time_text = TEXT_FONT.render(f"Time: {seconds//60}min{seconds%60}s", 1, BLACK)

    SCREEN.fill(GREY)  # Background

    SCREEN.blit(cleaned_text, (0, 0))  # Cleaned percent text
    SCREEN.blit(time_text, (0, cleaned_text.get_height()))  # Cleaned time text

    # Draw walls
    for w in walls:
        pygame.draw.line(SCREEN, BROWN, w, w)

    # Draw dust
    for d in dust:
        SCREEN.blit(DUST_IMAGE, d - np.array([DUST_WIDTH // 2, DUST_HEIGHT // 2]))

    rotate_and_blit(
        SCREEN,
        ROBOT_IMAGE,
        (round(x), round(y)),
        (ROBOT_LENGTH // 2, ROBOT_LENGTH // 2),
        np.rad2deg(theta),
    )  # Robot

    pygame.display.update()


def show_final_score(start_time, final_time):
    """Shows the final score"""

    message_text = TEXT_FONT.render(f"All cleaned!", 1, BLACK)
    seconds = round(final_time - start_time)
    time_text = TEXT_FONT.render(f"Time: {seconds//60}min{seconds%60}s", 1, BLACK)

    SCREEN.fill(GREY)  # Background

    SCREEN.blit(
        message_text,
        (
            (WIDTH - message_text.get_width()) // 2,
            (HEIGHT - message_text.get_height()) // 2,
        ),
    )  # Cleaned percent text
    SCREEN.blit(
        time_text,
        (
            (WIDTH - time_text.get_width()) // 2,
            (HEIGHT - time_text.get_height()) // 2 + message_text.get_height(),
        ),
    )  # Cleaned time text

    SCREEN.blit(
        TEXT_FONT.render(
            "Click anywhere to exit",
            1,
            BLACK,
        ),
        (0, 0),
    )
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            return


def rotate_and_blit(surf, image, pos, originPos, angle):
    """Helper function so a rotated image keeps dimensions"""

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
