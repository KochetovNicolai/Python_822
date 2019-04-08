import sys
import random
from gameInfo import *
from drawSomething import draw_score

GRAY = (32, 32, 32)


def sleep():
    cat = Cat()
    cat.status = Animations.sleep
    game_info = GameInfo()
    cat.anim_time = 0
    clock = pygame.time.Clock()
    # this range used to make frames lasted the same time
    for _ in range(game_info.tick_rate - game_info.tick_rate % len(
            cat.status.value)):
        clock.tick(game_info.tick_rate)
        game_info.screen.blit(
            pygame.transform.scale(game_info.background, (
                game_info.window_width, game_info.window_height)),
            (0, 0))
        draw_score()
        cat.draw()
    for cur_time in range(10 * game_info.tick_rate):
        clock.tick(game_info.tick_rate)
        if cur_time % game_info.tick_rate == 0:
            if cat.sleepy > 0:
                cat.sleepy -= 1
                if cur_time % (2 * game_info.tick_rate) == 0 and cat.tired > 0:
                    cat.tired -= 1
            else:
                return
        game_info.screen.blit(
            pygame.transform.scale(game_info.background, (
                game_info.window_width, game_info.window_height)), (0, 0))
        draw_score()
        game_info.screen.blit(
            pygame.transform.scale(Animations.sleep.value[6],
                                   (game_info.width * 4, game_info.height * 4)),
            (cat.x, cat.y))
        pygame.display.update()
        pygame.event.clear()


def run_cat_run():
    cat = Cat()
    cat.status = Animations.walk
    game_info = GameInfo()
    cat.anim_time = 0
    cat.x = 0
    cat.y = 6.7 * game_info.height
    cur_x = 0
    clock = pygame.time.Clock()
    run_time = 200  # to complete full screen in reasonable time
    for _ in range(run_time):
        clock.tick(game_info.tick_rate)
        bamboo_size = game_info.bamboo.get_size()
        # rescale bamboo picture to fit the screen and move
        game_info.screen.blit(pygame.transform.scale(game_info.bamboo, (
            game_info.window_height * bamboo_size[0] // bamboo_size[1],
            game_info.window_height)), (0, 0), (cur_x, 0, cur_x +
                                                bamboo_size[1] *
                                                game_info.width //
                                                game_info.height,
                                                bamboo_size[1]))
        cat.draw()
        cat.x += game_info.window_width // run_time
        cur_x += game_info.window_width // run_time

    game_info.screen.blit(pygame.transform.scale(game_info.background,
                                                 (game_info.window_width,
                                                  game_info.window_height)),
                          (0, 0))

    cat.x = 4 * game_info.width
    cat.y = 5 * game_info.height
    cat.anim_time = 0
    cat.idle_time = 0
    cat.status = Animations.idle

    cat.cardio += 2
    cat.tired += 1


def hit_bag():
    cat = Cat()
    game_info = GameInfo()
    cat.x = int(game_info.width * 6.8)
    if random.randint(1, 2) == 1:
        punching_bag()
    else:
        kicking_bag()
    cat.status = Animations.idle
    cat.x = game_info.width * 4
    cat.anim_time = 0
    cat.idle_time = 0


def punching_bag():
    cat = Cat()
    cat.status = Animations.punch
    game_info = GameInfo()
    cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(random.randint(2, 4) * game_info.tick_rate):
        clock.tick(game_info.tick_rate)
        game_info.screen.blit(
            pygame.transform.scale(game_info.background, (
                game_info.window_width, game_info.window_height)), (0, 0))
        draw_score()
        cat.draw()

    cat.muscle += 3
    cat.tired += 2


def kicking_bag():
    cat = Cat()
    cat.status = Animations.kick
    game_info = GameInfo()
    cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(random.randint(2, 4) * game_info.tick_rate):
        clock.tick(game_info.tick_rate)
        game_info.screen.blit(pygame.transform.scale(game_info.background,
                                                     (game_info.window_width,
                                                      game_info.window_height)),
                              (0, 0))
        draw_score()
        cat.draw()

    cat.muscle += 2
    cat.tired += 2


def die():
    cat = Cat()
    cat.status = Animations.dead
    game_info = GameInfo()
    cat.anim_time = 0
    clock = pygame.time.Clock()
    # this range used to make frames lasted the same time
    for _ in range(game_info.tick_rate - game_info.tick_rate % len(
            cat.status.value)):
        clock.tick(game_info.tick_rate)
        game_info.screen.blit(pygame.transform.scale(game_info.background, (
            game_info.window_width, game_info.window_height)), (0, 0))
        draw_score()
        cat.draw()

    font = pygame.font.SysFont("calibri", game_info.height, True)
    text = font.render("{} is dead".format(cat.name), True, GRAY)
    text_rect = text.get_rect()
    text_rect.center = (int(game_info.width * 5.5), game_info.height * 9)
    game_info.screen.blit(text, text_rect)

    font = pygame.font.SysFont("calibri", game_info.height // 2, True)
    text = font.render("PRESS ANY KEY TO CONTINUE", True, GRAY)
    text_rect = text.get_rect()
    text_rect.center = (int(game_info.width * 5.5), int(game_info.height * 9.7))
    game_info.screen.blit(text, text_rect)

    pygame.display.update()

    cat.reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return GameStatus.menu
