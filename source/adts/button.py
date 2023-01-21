import pygame


class Button:
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

        self.text = font.render(text, 1, text_color)
        self.border = 0.2
        self.rect = self.text.get_rect()
        self.rect.update(
            *coordinate,
            *(
                (1 + self.border) * self.text.get_width(),
                (1 + self.border) * self.text.get_height(),
            ),
        )
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface: pygame.Surface, mouse_pos: tuple):
        """Blits the button to the screen"""

        pygame.draw.rect(
            surface,
            self.hover_color if self.rect.collidepoint(mouse_pos) else self.color,
            self.rect,
        )

        # Center the text inside the rectangle
        surface.blit(
            self.text,
            (
                self.rect.topleft[0] + self.text.get_width() * self.border / 2,
                self.rect.topleft[1] + self.text.get_height() * self.border / 2,
            ),
        )

    def set_top_left_corner(self, x: int, y: int) -> None:
        """Changes rectangle top left corner position"""

        self.rect.move_ip(x - self.rect.topleft[0], y - self.rect.topleft[1])

    def get_height(self) -> int:
        """Getter for rectangle height"""

        return self.rect.height

    def get_width(self) -> int:
        """Getter for rectangle width"""

        return self.rect.width

    def get_text_height(self) -> int:
        """Getter for text height"""

        return self.text.get_height()

    def get_text_width(self) -> int:
        """Getter for text width"""

        return self.text.get_width()

    def get_border(self) -> float:
        """Getter for text border"""

        return self.border

    def __contains__(self, point: tuple) -> bool:
        """Checks if a point is inside the button"""

        return self.rect.collidepoint(point)
