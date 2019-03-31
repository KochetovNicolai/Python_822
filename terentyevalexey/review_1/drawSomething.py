from Game import *


def draw_cat(status):
    cat = Cat()
    game_info = GameInfo()
    if cat.anim_time >= game_info.tick_rate:
        cat.anim_time = 0

    cur_frame = cat.anim_time // (
            game_info.tick_rate //
            len(status.value))
    cat.anim_time += 1

    if cur_frame >= len(status.value):
        cat.anim_time = 0
        return
    game_info.screen.blit(
        pygame.transform.scale(status.value[cur_frame],
                               (game_info.width * 4, game_info.height * 4)),
        (cat.x, cat.y))
    pygame.display.update()


def draw_score():
    cat = Cat()
    game_info = GameInfo()
    font = pygame.font.SysFont("calibri", game_info.height // 2, bold=True)

    text = font.render(str(cat.tired), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 4, game_info.height * 4.35)
    game_info.screen.blit(text, text_rect)

    text = font.render(str(cat.muscle), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5, game_info.height * 4.05)
    game_info.screen.blit(text, text_rect)

    text = font.render(str(cat.cardio), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5.975, game_info.height * 4.35)
    game_info.screen.blit(text, text_rect)

    text = font.render(str(cat.sleepy), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 6.975, game_info.height * 4.05)
    game_info.screen.blit(text, text_rect)


def draw_menu(pos=0):
    cat = Cat()
    game_info = GameInfo()
    game_info.screen.fill((32, 32, 32))
    # draw game name
    font = pygame.font.SysFont("calibri", game_info.height, bold=True)
    text = font.render(cat.name, True, (100, 100, 100))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5, game_info.height * 1.5)
    game_info.screen.blit(text, text_rect)

    font = pygame.font.SysFont("calibri", game_info.height // 2, bold=True)

    # play draw
    pygame.draw.rect(game_info.screen, (0, 128, 0),
                     (game_info.width * 4, game_info.height * 3,
                      2 * game_info.width, game_info.height))
    text = font.render("START A GAME", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5, game_info.height * 3.55)
    game_info.screen.blit(text, text_rect)

    # options draw
    pygame.draw.rect(game_info.screen, (102, 153, 153),
                     (game_info.width * 4, game_info.height * 5,
                      2 * game_info.width, game_info.height))
    text = font.render("OPTIONS", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5, game_info.height * 5.55)
    game_info.screen.blit(text, text_rect)

    # exit game draw
    pygame.draw.rect(game_info.screen, (128, 0, 0),
                     (game_info.width * 4, game_info.height * 7,
                      2 * game_info.width, game_info.height))
    text = font.render("EXIT", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5, game_info.height * 7.55)
    game_info.screen.blit(text, text_rect)

    game_info.screen.blit(
        pygame.transform.scale(game_info.arrow,
                               (game_info.height, game_info.height)),
        (game_info.width * 3.3, game_info.height * (3 + 2 * pos)))

    pygame.display.update()


def draw_options(pos=0):
    game_info = GameInfo()
    game_info.screen.fill((32, 32, 32))
    font = pygame.font.SysFont("calibri", game_info.height // 2, bold=True)

    # fullscreen draw
    pygame.draw.rect(game_info.screen, (102, 153, 153),
                     (game_info.width * 4, game_info.height * 3.5,
                      2 * game_info.width, game_info.height))
    text = font.render("FULLSCREEN", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5, game_info.height * 4.05)
    game_info.screen.blit(text, text_rect)

    # menu button draw
    pygame.draw.rect(game_info.screen, (102, 153, 153),
                     (game_info.width * 4, game_info.height * 5.5,
                      2 * game_info.width, game_info.height))
    text = font.render("BACK TO MENU", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5, game_info.height * 6.05)
    game_info.screen.blit(text, text_rect)

    game_info.screen.blit(
        pygame.transform.scale(game_info.arrow,
                               (game_info.height, game_info.height)),
        (game_info.width * 3.3, game_info.height * (3.5 + 2 * pos)))

    pygame.display.update()
