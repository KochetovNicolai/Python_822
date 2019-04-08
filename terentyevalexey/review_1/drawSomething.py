from gameInfo import *

GRAY = (32, 32, 32)
GREEN = (0, 128, 0)
LIGHTGRAY = (128, 128, 128)
COOLCOLOR = (103, 153, 153)
RED = (128, 0, 0)


def draw_score():
    cat = Cat()
    game_info = GameInfo()
    font = pygame.font.SysFont("calibri", game_info.height // 2, bold=True)

    text = font.render(str(cat.tired), True, GRAY)
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 4, int(game_info.height * 4.35))
    game_info.screen.blit(text, text_rect)

    text = font.render(str(cat.muscle), True, GRAY)
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5, int(game_info.height * 4.05))
    game_info.screen.blit(text, text_rect)

    text = font.render(str(cat.cardio), True, GRAY)
    text_rect = text.get_rect()
    text_rect.center = (int(game_info.width * 5.975),
                        int(game_info.height * 4.35))
    game_info.screen.blit(text, text_rect)

    text = font.render(str(cat.sleepy), True, GRAY)
    text_rect = text.get_rect()
    text_rect.center = (int(game_info.width * 6.975),
                        int(game_info.height * 4.05))
    game_info.screen.blit(text, text_rect)
