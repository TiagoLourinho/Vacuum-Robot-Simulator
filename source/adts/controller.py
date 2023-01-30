import numpy as np
import pygame

from .robot import VacuumRobot


class Controller:
    """Controls the robot"""

    def __init__(
        self, linear_velocity: float, angular_velocity: float, mode: str, frequency: int
    ) -> None:
        self.automatic = mode == "automatic"
        self.default = np.array([linear_velocity, angular_velocity])
        self.frequency = frequency

        self.state = "walking"  # Current state from : walking, rotating
        self.wall_state = (
            "looking"  # Current wall state from: following, contorning, looking
        )
        self.start_angle = None  # Start angle when contorning a wall
        self.start_pos = None  # Start pos when contorning a wall
        self.collided = False  # If collided before

        self.rotating_timer = None  # Timer for rotating
        self.n_frames = 0  # Counter to use in timer

        # Set current controls and vacuum motors
        if self.automatic:
            self.controls = np.array([linear_velocity, 0])
            self.motors = True
        else:
            self.controls = np.array([0, 0])
            self.motors = False

    def get_controls(
        self, keys: list, back_lidar: bool, front_lidar: bool, robot: VacuumRobot
    ) -> np.array:
        """Get current controls"""

        x, y, theta = robot.get_state()

        if self.automatic:

            match self.wall_state:
                case "following":
                    match self.state:
                        case "walking":
                            # Is walking but lost track of the wall
                            if not back_lidar and not front_lidar:
                                self.set_controls("rotating", direction=-1, timer=False)
                                self.wall_state = "contorning"
                                self.start_angle = theta

                case "contorning":
                    match self.state:
                        case "walking":
                            # Found the wall
                            if back_lidar and front_lidar:
                                self.wall_state = "following"
                            # Avoid infinite walking forward (limit)
                            elif (
                                self.start_pos is not None
                                and np.linalg.norm(np.array([x, y]) - self.start_pos)
                                > 2 * robot.get_radius()
                            ):
                                self.start_pos = None
                                self.set_controls("rotating", direction=-1, timer=False)
                                self.start_angle = theta
                        case "rotating":

                            # Stop rotating when the limit was reached or the front lidar found the wall
                            if (
                                not self.collided
                                and self.start_angle is not None
                                and (
                                    front_lidar
                                    or np.abs(theta - self.start_angle) > np.pi / 2
                                )
                            ):
                                self.start_angle = None
                                self.set_controls("walking")
                                self.start_pos = np.array([x, y])

                case "looking":
                    # Found wall
                    if back_lidar and front_lidar:
                        self.wall_state = "following"

            # Rotating timer expired
            if self.rotating_timer is not None and self.n_frames >= max(
                self.rotating_timer, 1
            ):
                self.set_controls("walking")

            if self.rotating_timer is not None:
                self.n_frames += 1

            self.collided = False

        else:
            if keys[pygame.K_w]:
                self.controls = np.array([self.default[0], 0])
            elif keys[pygame.K_a]:
                self.controls = np.array([0, self.default[1]])
            elif keys[pygame.K_s]:
                self.controls = np.array([-self.default[0], 0])
            elif keys[pygame.K_d]:
                self.controls = np.array([0, -self.default[1]])
            elif keys[pygame.K_RETURN]:
                self.controls = np.array([0, 0])

            self.motors = keys[pygame.K_SPACE]

        return self.controls, self.motors

    def collide(self) -> None:
        """Changes control after colision"""

        if self.automatic:
            self.collided = True
            if self.rotating_timer is None:
                self.set_controls("rotating", direction=1)

    def get_timer_in_frames(self, rotate_percent: float) -> int:
        """Returns a timer in frames"""

        return round(self.frequency * rotate_percent * np.pi / self.default[1])

    def set_controls(self, action: str, direction: int = None, timer=True) -> None:
        """Sets the current controls"""

        if action == "walking":
            self.controls = np.array([self.default[0], 0])
            self.motors = True
            self.rotating_timer = None

        elif action == "rotating":
            self.controls = np.array([0, direction * self.default[1]])
            self.motors = False
            self.rotating_timer = (
                self.get_timer_in_frames(rotate_percent=0.01) if timer else None
            )

        self.state = action
        self.n_frames = 0
