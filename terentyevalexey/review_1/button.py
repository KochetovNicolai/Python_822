import pygame

BLACK = (0, 0, 0)
CALIBRI = 'calibri'


class Button:
    """
    creates a button from font, text and center info
    """

    def __init__(self, text, color, rectangle):
        """
        :param text: button text
        :param color: color of button
        :param rectangle: pygame rectangle
        """
        self.rectangle = pygame.Rect(rectangle)
        self.color = color
        font_division_ratio = 2  # font size is this times less than rectangle
        text_y_shift = 0.04  # to center the text for perfectionists
        font_height = self.rectangle.height // font_division_ratio
        self.font = pygame.font.SysFont(CALIBRI, font_height, True)
        self.text = self.font.render(text, True, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.rectangle.centerx
        self.text_rect.centery = self.rectangle.centery + int(
            self.rectangle.height * text_y_shift)

    def draw(self, surface):
        """
        :param surface: surface to blit a button on
        """
        pygame.draw.rect(surface, self.color, self.rectangle)
        surface.blit(self.text, self.text_rect)

    def has(self, *point):
        """
        :param point: pair of coordinates
        :return: True if point is in the button rectangular
        """
        return self.rectangle.collidepoint(*point)
