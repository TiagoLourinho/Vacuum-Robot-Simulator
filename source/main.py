import pygame
import time

from adts import *
from constants import *
from utils import *


def main():

    ##### Loading game ###
    show_loading_screen()
    mode = choose_game_mode()
    walls = draw_walls(WALL_SIZE)

    ##### Init game state #####
    house = House(WIDTH, HEIGHT, walls)

    if not are_walls_valid(house):
        house = House(WIDTH, HEIGHT, DEFAULT_WALLS)
        walls = DEFAULT_WALLS

    walls_group = pygame.sprite.Group()
    for w in walls:
        walls_group.add(Wall(BROWN, *w))

    controller = Controller(LINEAR_VELOCITY, ANGULAR_VELOCITY, mode, FREQUENCY)

    # Get a valid starting position for the robot
    while True:
        robot_pos = house.get_free_spot()
        robot = VacuumRobot(ROBOT_IMAGE, ROBOT_LENGTH // 2, *robot_pos)
        if not pygame.sprite.spritecollideany(robot, walls_group):
            break

    dust_group = pygame.sprite.Group()
    for _ in range(N_DUST):
        while True:
            d = house.get_free_spot()
            dust = Dust(DUST_IMAGE, *d)
            if not pygame.sprite.spritecollideany(dust, walls_group):
                break
        house.dirty(*d)
        dust_group.add(dust)

    init_screen(robot, walls_group, dust_group)

    ##### Main game loop #####
    clock = pygame.time.Clock()
    vacuum_sound_is_playing = False
    start_time = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # All cleaned
        if not dust_group:
            if vacuum_sound_is_playing:
                VACUUM_SOUND.stop()
            break

        controls, vacuuming = controller.get_controls(
            pygame.key.get_pressed(),
            house.is_following_wall(robot, "back"),
            house.is_following_wall(robot, "front"),
            robot,
        )

        robot.move(controls, 1 / FREQUENCY)

        # Vacuum
        if vacuuming:
            for vacuumed in pygame.sprite.spritecollide(robot, dust_group, dokill=True):
                house.clean(*vacuumed.get_pos())

        walls_collided = pygame.sprite.spritecollide(robot, walls_group, dokill=False)

        # Hit wall
        if walls_collided:

            # Compensante for the robot being represented as a rectangle
            for w in walls_collided:
                if np.linalg.norm(w.pos - robot.get_state()[:2]) <= robot.get_radius():
                    if mode == "manual":
                        COLLISION_SOUND.play()
                    controller.collide()
                    robot.collided()

                    break
        # Left screen
        elif not robot.get_rect() in SCREEN.get_rect():
            if mode == "manual":
                COLLISION_SOUND.play()
            controller.collide()
            robot.collided()

        # Vacuum sound management
        if vacuuming and not vacuum_sound_is_playing:
            VACUUM_SOUND.play(-1)
            vacuum_sound_is_playing = True
        elif not vacuuming:
            VACUUM_SOUND.stop()
            vacuum_sound_is_playing = False

        draw_screen(robot, walls_group, dust_group, start_time)
        clock.tick(FREQUENCY)

    show_final_score(start_time, time.time())


if __name__ == "__main__":
    main()
