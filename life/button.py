import field
import pygame


class Button:
    BACKGROUND = (133, 133, 133)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 139, 139)

    widht = 140
    margin = 5

    def __init__(self, txt, font, font_size, x, y, color=field.Field.WHITE, background=BLUE):
        self.text = txt
        self.font = pygame.font.SysFont(font, font_size)
        self.x = x
        self.y = y
        self.color = color
        self.background = background

    def draw(self, surface, is_rect=True):
        text_sur = self.get_surface(self.text)

        if is_rect:
            pygame.draw.rect(
                surface,
                self.background,
                (self.x, self.y, Button.widht, self.y)
            )

        surface.blit(text_sur, (self.x, self.y))

    def get_surface(self, text):
        text_surface = self.font.render(text,
                                        False,
                                        self.color)
        return text_surface
