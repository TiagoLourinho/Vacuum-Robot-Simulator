import pygame
import time

from adts import House, VacuumRobot, Controller
from constants import *
from utils import *


def main():
    start_time = time.time()

    mode = choose_game_mode()
    walls = draw_walls()

    house = House(WIDTH, HEIGHT, walls, DEFAULT_WALLS)
    robot = VacuumRobot(
        ROBOT_LENGTH // 2, *house.get_charging_station_location(ROBOT_LENGTH)
    )
    controller = Controller(LINEAR_VELOCITY, ANGULAR_VELOCITY, mode)

    house.generate_dust(N_DUST, DUST_WIDTH, DUST_HEIGHT)

    init_screen(house, robot)

    clock = pygame.time.Clock()

    vacuum_sound_is_playing = False

    while True:
        clock.tick(FREQUENCY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # All cleaned
        if int(100 * (N_DUST - len(house.get_dust_spots())) / N_DUST) == 100:
            break

        controls, vacuum = controller.get_controls(pygame.key.get_pressed())

        robot.move(controls, 1 / FREQUENCY)

        # Vacuum
        if vacuum:
            for vacuumed in robot.vacuum(house.get_dust_spots()):
                house.clean(*vacuumed)

        # Hit wall
        if robot.hits_wall(house.get_wall_spots()):
            COLLISION_SOUND.play()
            controller.collided()

        # Vacuum sound management
        if vacuum and not vacuum_sound_is_playing:
            VACUUM_SOUND.play(-1)
            vacuum_sound_is_playing = True
        elif not vacuum:
            VACUUM_SOUND.stop()
            vacuum_sound_is_playing = False

        draw_screen(house, robot, start_time)

    show_final_score(start_time, time.time())


if __name__ == "__main__":
    main()
