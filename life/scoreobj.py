import pygame
import button
import menu


class ScoreObj(button.Button):

    def __init__(self, x, y):
        super().__init__('score', menu.Menu.FONT, menu.Menu.FONT_SIZE, x, y)

    def draw(self, surface, field):
        text_sur = self.get_surface(str(field.live_cells))

        pygame.draw.rect(
            surface,
            button.Button.BLUE,
            (self.x, self.y, button.Button.widht, self.y)
        )

        surface.blit(text_sur, (self.x, self.y))
