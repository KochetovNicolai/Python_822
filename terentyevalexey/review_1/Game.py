"""Игра про кота-качка. Кот хочет накачаться, помоги ему!
Коту нужно бить грушу, чтобы качать руки и ноги.
Так же коту нужно бегать, чтобы не перенапрягать мышцы,
а ещё ему необходимо отдыхать, чтобы не умереть.
"""

import random
import sys
from gameInfo import *

if __name__ == '__main__':
    from menu import main_menu, options
    from actions import *
    from drawSomething import draw_cat, draw_score
    logo = pygame.image.load(os.path.join('data', 'logo.png'))
    pygame.init()
    pygame.display.set_caption("cat")
    pygame.display.set_icon(logo)


def main_loop():
    cat = Cat()
    game_info = GameInfo()
    game_info.screen.blit(
        pygame.transform.scale(game_info.background,
                               (game_info.width * 10, game_info.height * 10)),
        (0, 0))
    clock = pygame.time.Clock()

    status = Animations.idle
    cat.idle_time = 0
    pygame.time.set_timer(pygame.USEREVENT + 1, 6000)  # cat sleepy inc timer
    pygame.time.set_timer(pygame.USEREVENT + 2, 8000)  # cat muscle dec timer
    pygame.time.set_timer(pygame.USEREVENT + 3, 12000)  # cat cardio dec timer

    while True:
        clock.tick(game_info.tick_rate)

        if cat.muscle > 30:
            cat.muscle -= 1
        if cat.cardio > 30:
            cat.cardio -= 1

        game_info.screen.blit(
            pygame.transform.scale(game_info.background, (
                game_info.width * 10, game_info.height * 10)), (0, 0))
        draw_score()
        draw_cat(status)

        if cat.sleepy >= 20:
            sleep()
        if cat.tired > 10:
            return die()

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                cat.sleepy += 1
            if event.type == pygame.USEREVENT + 2:
                if cat.muscle > 0:
                    cat.muscle -= 1
            if event.type == pygame.USEREVENT + 3:
                if cat.cardio > 0:
                    cat.cardio -= 1

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                elif pygame.key.get_mods() & pygame.KMOD_ALT and \
                        event.key == pygame.K_F4:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN or \
                        event.key == pygame.K_KP_ENTER:
                    run_cat_run()

                elif event.key == pygame.K_SPACE:
                    cat.x = game_info.width * 6.8
                    if random.randint(1, 2) == 1:
                        punching_bag()
                    else:
                        kicking_bag()
                    status = Animations.idle
                    cat.x = game_info.width * 4
                    cat.anim_time = 0
                    cat.idle_time = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    mx, my = pygame.mouse.get_pos()
                    if (mx > game_info.width * 9) and (
                            game_info.height * 6 < my < game_info.height * 9.5):
                        cat.x = game_info.width * 6.8
                        if random.randint(1, 2) == 1:
                            punching_bag()
                        else:
                            kicking_bag()
                        status = Animations.idle
                        cat.x = game_info.width * 4
                        cat.anim_time = 0
                        cat.idle_time = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if status != Animations.walk:
                cat.anim_time = 0
                status = Animations.walk
            cat.x += game_info.width // 10

        elif keys[pygame.K_LEFT]:
            if status != Animations.walk_left:
                cat.anim_time = 0
                status = Animations.walk_left
            cat.x -= game_info.width // 10

        elif status != Animations.idle:
            status = Animations.idle
            cat.anim_time = 0
            cat.idle_time = 0

        if status == Animations.idle:
            cat.idle_time += 1
            if cat.idle_time == game_info.tick_rate * 5 and cat.tired > 0:
                cat.tired -= 1
                cat.idle_time = 0

        if cat.x >= game_info.width * 6.8:
            cat.x = game_info.width * 6.8
            if random.randint(1, 2) == 1:
                punching_bag()
            else:
                kicking_bag()
            status = Animations.idle
            cat.x = game_info.width * 4
            cat.anim_time = 0
            cat.idle_time = 0

        if cat.x <= - 2 * game_info.width:
            run_cat_run()
            status = Animations.idle
            cat.x = game_info.width * 4
            cat.anim_time = 0
            cat.idle_time = 0

        pygame.event.clear()


if __name__ == '__main__':
    cur_state = 0
    while cur_state is not None:
        if cur_state == 0:
            cur_state = main_menu()
        elif cur_state == 1:
            cur_state = options()
        elif cur_state == 2:
            cur_state = main_loop()
