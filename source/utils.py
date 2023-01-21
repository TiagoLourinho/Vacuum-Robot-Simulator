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

    # Blit and update
    SCREEN.fill(PY_GREEN)
    SCREEN.blit(text, text_rect)
    SCREEN.blit(image, image_rect)

    pygame.display.update()
    pygame.time.delay(2000)


def choose_game_mode():
    """Chooses the game mode to play"""

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

    SCREEN.fill(GREY)
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

        if left_click:

            # Automatic control
            if pos in automatic_button:

                text = TEXT_FONT.render(
                    "The robot will be automatically controlled",
                    1,
                    BLACK,
                )

                SCREEN.fill(GREY)
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

                wait_for_click()
                return "automatic"

            elif pos in manual_button:

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

                SCREEN.fill(GREY)

                offset = 0
                x_offset = text[0].get_width()  # Align text
                for t in text:
                    SCREEN.blit(
                        t,
                        (
                            (WIDTH - x_offset) // 2,
                            (HEIGHT - t.get_height()) // 2 + offset,
                        ),
                    )

                    # Bigger offset in the first one
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

                wait_for_click()
                return "manual"

        automatic_button.draw(SCREEN, pos)
        manual_button.draw(SCREEN, pos)
        pygame.display.update()


def draw_walls(size):
    """Lets the player draw the walls"""

    start_button = Button(TEXT_FONT, "Start Game", BLACK, BLUE, LIGHT_BLUE, (5, 5))

    instruction_text = TEXT_FONT.render(
        "Draw the house walls (or don't, to use the default)", 1, BLACK
    )

    SCREEN.fill(GREY)
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
                for x in range(-size // 2, size // 2 + 1):
                    for y in range(-size // 2, size // 2 + 1):
                        cur = (min(pos[0] + x, WIDTH - 1), min(pos[1] + y, HEIGHT - 1))
                        walls.append(cur)
                        pygame.draw.line(SCREEN, BROWN, cur, cur)

        start_button.draw(SCREEN, pos)
        pygame.display.update()


def init_screen(
    robot: VacuumRobot,
    walls_group: pygame.sprite.Group,
    dust_group: pygame.sprite.Group,
) -> None:
    """Initializes the screen"""

    SCREEN.fill(GREY)

    walls_group.draw(SCREEN)

    pygame.display.update()
    pygame.time.delay(100)

    # Draw dust
    for d in dust_group:
        d.draw(SCREEN)
        pygame.display.update()
        pygame.time.delay(10)

    robot.draw(SCREEN)

    pygame.display.update()
    pygame.time.delay(500)


def draw_screen(
    robot: VacuumRobot,
    walls_group: pygame.sprite.Group,
    dust_group: pygame.sprite.Group,
    start_time,
) -> None:
    """Draws the general game screen"""

    # Text
    cleaned_text = TEXT_FONT.render(
        f"Cleaned: {int(100*(N_DUST-len(dust_group))/N_DUST)}%", 1, BLACK
    )
    seconds = round(time.time() - start_time)
    time_text = TEXT_FONT.render(f"Time: {seconds//60}min{seconds%60}s", 1, BLACK)

    SCREEN.fill(GREY)  # Background

    SCREEN.blit(cleaned_text, (0, 0))  # Cleaned percent text
    SCREEN.blit(time_text, (0, cleaned_text.get_height()))  # Cleaned time text

    walls_group.draw(SCREEN)
    dust_group.draw(SCREEN)
    robot.draw(SCREEN)

    pygame.display.update()


def show_final_score(start_time, final_time):
    """Shows the final score"""

    font = pygame.font.SysFont("comicsans", 70)
    message_text = font.render(f"All cleaned!", 1, BLACK)
    seconds = round(final_time - start_time)
    time_text = font.render(f"Time: {seconds//60}min{seconds%60}s", 1, BLACK)

    SCREEN.fill(PY_GREEN)  # Background

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
            "Click anywhere to quit",
            1,
            BLACK,
        ),
        (0, 0),
    )
    pygame.display.update()

    wait_for_click()


def are_walls_valid(house: House, max_tries=1000) -> bool:
    """Checks if the walls are valid"""

    min_x, max_x, min_y, max_y = house.get_surrounding_rectangle()

    tries = 0
    while tries < max_tries:

        x = np.random.randint(min_x + 1, max_x)
        y = np.random.randint(min_y + 1, max_y)

        # Generate a spot for robot without walls, dust and inside the house
        if house.is_inside_house(x, y):

            return True

        tries += 1

    return False


def wait_for_click() -> None:
    """Waits for the player to click the screen"""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            pygame.time.delay(100)
            return
