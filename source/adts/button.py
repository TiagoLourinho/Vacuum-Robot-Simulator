import pygame


class Button(pygame.sprite.Sprite):
    """Represents a clickable button"""

    def __init__(
        self,
        font: pygame.font.Font,
        text: str,
        text_color: tuple,
        color: tuple,
        hover_color: tuple,
        coordinate: tuple = (0, 0),
    ) -> None:
        super(Button, self).__init__()

        self.__text = font.render(text, 1, text_color)
        self.__border = 0.2
        self.__rect = self.__text.get_rect()
        self.__rect.update(
            *coordinate,
            *(
                (1 + self.__border) * self.__text.get_width(),
                (1 + self.__border) * self.__text.get_height(),
            ),
        )
        self.__color = color
        self.__hover_color = hover_color

    def draw(self, surface: pygame.Surface, mouse_pos: tuple):
        """Blits the button to the screen"""

        pygame.draw.rect(
            surface,
            self.__hover_color if self.__rect.collidepoint(mouse_pos) else self.__color,
            self.__rect,
        )

        # Center the text inside the rectangle
        surface.blit(
            self.__text,
            (
                self.__rect.topleft[0] + self.__text.get_width() * self.__border / 2,
                self.__rect.topleft[1] + self.__text.get_height() * self.__border / 2,
            ),
        )

    def set_top_left_corner(self, x: int, y: int) -> None:
        """Changes rectangle top left corner position"""

        self.__rect.move_ip(x - self.__rect.topleft[0], y - self.__rect.topleft[1])

    def get_height(self) -> int:
        """Getter for rectangle height"""

        return self.__rect.height

    def get_width(self) -> int:
        """Getter for rectangle width"""

        return self.__rect.width

    def get_text_height(self) -> int:
        """Getter for text height"""

        return self.__text.get_height()

    def get_text_width(self) -> int:
        """Getter for text width"""

        return self.__text.get_width()

    def get_border(self) -> float:
        """Getter for text border"""

        return self.__border

    def __contains__(self, point: tuple) -> bool:
        """Checks if a point is inside the button"""

        return self.__rect.collidepoint(point)
