import pygame
import colours
import field


class Button:

    widht = 140
    height = 30
    margin = 5

    def __init__(self, txt, font, font_size, x, y, color=colours.WHITE, background=colours.BLUE):
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

    def is_inside(self, mouse_pos):
        if (
                self.x < mouse_pos[0] < self.x + Button.widht and
                self.y < mouse_pos[1] < self.y + Button.height
        ):
            return True
        else:
            return False
