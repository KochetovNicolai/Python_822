from Game import *
from drawSomething import draw_score, draw_cat


def sleep():
    cat = Cat()
    game_info = GameInfo()
    cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(game_info.tick_rate - game_info.tick_rate % len(
            Animations.sleep.value)):
        clock.tick(game_info.tick_rate)
        game_info.screen.blit(
            pygame.transform.scale(game_info.background, (
                game_info.width * 10, game_info.height * 10)),
            (0, 0))
        draw_score()
        draw_cat(Animations.sleep)
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
                game_info.width * 10, game_info.height * 10)), (0, 0))
        draw_score()
        game_info.screen.blit(
            pygame.transform.scale(Animations.sleep.value[6],
                                   (game_info.width * 4, game_info.height * 4)),
            (cat.x, cat.y))
        pygame.display.update()
        pygame.event.clear()


def run_cat_run():
    cat = Cat()
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
        game_info.screen.blit(pygame.transform.scale(game_info.bamboo, (
            game_info.height * 10 * bamboo_size[0] // bamboo_size[1],
            game_info.height * 10)), (0, 0), (cur_x, 0, cur_x + bamboo_size[1] *
                                              game_info.width //
                                              game_info.height, bamboo_size[1]))
        draw_cat(Animations.walk)
        cat.x += game_info.width * 10 // run_time
        cur_x += game_info.width * 10 // run_time

    game_info.screen.blit(
        pygame.transform.scale(game_info.background,
                               (game_info.width * 10, game_info.height * 10)),
        (0, 0))

    cat.x = 4 * game_info.width
    cat.y = 5 * game_info.height
    cat.anim_time = 0

    cat.cardio += 2
    cat.tired += 1


def punching_bag():
    cat = Cat()
    game_info = GameInfo()
    cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(random.randint(2, 4) * game_info.tick_rate):
        clock.tick(game_info.tick_rate)
        game_info.screen.blit(
            pygame.transform.scale(game_info.background, (
                game_info.width * 10, game_info.height * 10)), (0, 0))
        draw_score()
        draw_cat(Animations.punch)

    cat.muscle += 3
    cat.tired += 2


def kicking_bag():
    cat = Cat()
    game_info = GameInfo()
    cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(random.randint(2, 4) * game_info.tick_rate):
        clock.tick(game_info.tick_rate)
        game_info.screen.blit(
            pygame.transform.scale(game_info.background,
                                   (game_info.width * 10,
                                    game_info.height * 10)),
            (0, 0))
        draw_score()
        draw_cat(Animations.kick)

    cat.muscle += 2
    cat.tired += 2


def die():
    cat = Cat()
    game_info = GameInfo()
    cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(game_info.tick_rate // 7 * 7):
        clock.tick(game_info.tick_rate)
        game_info.screen.blit(
            pygame.transform.scale(game_info.background, (
                game_info.width * 10, game_info.height * 10)), (0, 0))
        draw_score()
        draw_cat(Animations.dead)

    font = pygame.font.SysFont("calibri", game_info.height, bold=True)
    text = font.render("{} is dead".format(cat.name), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5.5, game_info.height * 9)
    game_info.screen.blit(text, text_rect)

    font = pygame.font.SysFont("calibri", game_info.height // 2, bold=True)
    text = font.render("PRESS ANY KEY TO CONTINUE", True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (game_info.width * 5.5, game_info.height * 9.7)
    game_info.screen.blit(text, text_rect)

    pygame.display.update()

    cat.reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return 0
