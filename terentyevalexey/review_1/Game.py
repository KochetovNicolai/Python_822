"""Игра про кота-качка. Кот хочет накачаться, помоги ему!
Коту нужно бить грушу, чтобы качать руки и ноги.
Так же коту нужно бегать, чтобы не перенапрягать мышцы,
а ещё ему необходимо отдыхать, чтобы не умереть.
"""

import random
import pygame
import sys
import os
from singleton import singleton

if __name__ == '__main__':
    logo = pygame.image.load(os.path.join('data', 'logo.png'))
    pygame.init()
    pygame.display.set_caption("cat")
    pygame.display.set_icon(logo)


@singleton
class GameInfo:
    def __init__(self):
        self.background = pygame.image.load(
            os.path.join('data', 'background.jpg'))
        self.arrow = pygame.image.load(os.path.join('data', 'arrow.png'))
        self.bamboo = pygame.image.load(os.path.join('data', 'bamboo.jpg'))
        self.display_inf = pygame.display.Info()
        self.width = self.display_inf.current_w // 20
        self.height = self.display_inf.current_h // 20
        self.full_screen = False
        self.tick_rate = 30
        self.screen = pygame.display.set_mode(
            (self.width * 10, self.height * 10))


@singleton
class Cat:
    def __init__(self):
        self.name = "Kitty"
        game_info = GameInfo()
        self.x = game_info.width * 4
        self.y = game_info.height * 5
        self.anim_time = 0
        self.idle_time = 0

        self.cardio = 0
        self.muscle = 0
        self.tired = 0
        self.sleepy = 0
        self.animations = {
            "idle": [
                pygame.image.load(
                    os.path.join('data', 'cat', 'idle_{}.png'.format(i)))
                for i in range(1, 5)],
            "dead": [
                pygame.image.load(
                    os.path.join('data', 'cat', 'dead_{}.png'.format(i)))
                for i in range(1, 8)],
            "kick": [
                pygame.image.load(
                    os.path.join('data', 'cat', 'kick_{}.png'.format(i)))
                for i in range(1, 9)],
            "punch": [
                pygame.image.load(
                    os.path.join('data', 'cat', 'punch_{}.png'.format(i)))
                for i in range(1, 7)],
            "walk": [
                pygame.image.load(
                    os.path.join('data', 'cat', 'walk_{}.png'.format(i)))
                for i in range(1, 9)],
            "walk_left": [
                pygame.image.load(
                    os.path.join('data', 'cat', 'walk_left_{}.png'.format(i)))
                for i in range(1, 9)],
            "sleep": [
                pygame.image.load(
                    os.path.join('data', 'cat', 'sleep_{}.png'.format(i)))
                for i in range(1, 8)]
        }

    def reset(self):
        self.name = "Kitty"
        game_info = GameInfo()
        self.x = game_info.width * 4
        self.y = game_info.height * 5
        self.anim_time = 0
        self.idle_time = 0
        self.cardio = 0
        self.muscle = 0
        self.tired = 0
        self.sleepy = 0


def sleep():
    cat = Cat()
    game_info = GameInfo()
    cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(game_info.tick_rate // 7 * 7):
        clock.tick(game_info.tick_rate)
        game_info.screen.blit(
            pygame.transform.scale(game_info.background, (
                game_info.width * 10, game_info.height * 10)),
            (0, 0))
        draw_score()
        draw_cat("sleep")
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
        game_info.screen.blit(pygame.transform.scale(cat.animations["sleep"][6],
                                                     (game_info.width * 4,
                                                      game_info.height * 4)),
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
    for _ in range(200):
        clock.tick(game_info.tick_rate)
        game_info.screen.blit(
            pygame.transform.scale(game_info.bamboo, (
                game_info.height * 48, game_info.height * 10)), (0, 0),
            (cur_x, 0, cur_x + 2133, 1200))
        draw_cat("walk")
        cat.x += game_info.width // 20
        cur_x += game_info.width // 20

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
        draw_cat("punch")

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
        draw_cat("kick")

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
        draw_cat("dead")

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
                return main_menu()


def draw_cat(status):
    cat = Cat()
    game_info = GameInfo()
    if cat.anim_time >= game_info.tick_rate:
        cat.anim_time = 0

    cur_frame = cat.anim_time // (
            game_info.tick_rate //
            len(cat.animations[status]))
    cat.anim_time += 1
    if cur_frame >= len(cat.animations[status]):
        cat.anim_time = 0
        return
    game_info.screen.blit(
        pygame.transform.scale(cat.animations[status][cur_frame],
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


def main_loop():
    cat = Cat()
    game_info = GameInfo()
    game_info.screen.blit(
        pygame.transform.scale(game_info.background,
                               (game_info.width * 10, game_info.height * 10)),
        (0, 0))
    clock = pygame.time.Clock()

    status = "idle"
    cat.idle_time = 0
    pygame.time.set_timer(pygame.USEREVENT + 1, 6000)  # cat sleepy inc
    pygame.time.set_timer(pygame.USEREVENT + 2, 8000)  # cat muscle dec
    pygame.time.set_timer(pygame.USEREVENT + 3, 12000)  # cat cardio dec

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
                    return main_menu()
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
                    status = "idle"
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
                        status = "idle"
                        cat.x = game_info.width * 4
                        cat.anim_time = 0
                        cat.idle_time = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if status != "walk":
                cat.anim_time = 0
                status = "walk"
            cat.x += game_info.width // 10

        elif keys[pygame.K_LEFT]:
            if status != "walk_left":
                cat.anim_time = 0
                status = "walk_left"
            cat.x -= game_info.width // 10

        elif status != "idle":
            status = "idle"
            cat.anim_time = 0
            cat.idle_time = 0

        if status == "idle":
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
            status = "idle"
            cat.x = game_info.width * 4
            cat.anim_time = 0
            cat.idle_time = 0

        if cat.x <= - 2 * game_info.width:
            run_cat_run()
            status = "idle"
            cat.x = game_info.width * 4
            cat.anim_time = 0
            cat.idle_time = 0

        pygame.event.clear()


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


def options():
    cur_pose = 0
    game_info = GameInfo()
    draw_options()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    mx, my = pygame.mouse.get_pos()
                    if (game_info.width * 6 > mx > game_info.width * 4) and (
                            game_info.height * 4.5 > my >
                            game_info.height * 3.5):
                        if not game_info.full_screen:
                            game_info.screen = pygame.display.set_mode(
                                (game_info.width * 10, game_info.height * 10),
                                pygame.FULLSCREEN)
                            game_info.full_screen = True
                        else:
                            game_info.screen = pygame.display.set_mode(
                                (game_info.width * 10, game_info.height * 10))
                            game_info.full_screen = False
                        draw_options()
                        pygame.display.update()
                    elif (game_info.width * 6 > mx > game_info.width * 4) and (
                            game_info.height * 6.5 > my >
                            game_info.height * 5.5):
                        return main_menu()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if cur_pose < 1:
                        cur_pose += 1
                        draw_options(cur_pose)
                elif event.key == pygame.K_UP:
                    if cur_pose > 0:
                        cur_pose -= 1
                        draw_options(cur_pose)
                elif event.key == pygame.K_RETURN or \
                        event.key == pygame.K_KP_ENTER or \
                        event.key == pygame.K_SPACE:
                    if cur_pose == 0:
                        if not game_info.full_screen:
                            game_info.screen = pygame.display.set_mode(
                                (game_info.width * 10, game_info.height * 10),
                                pygame.FULLSCREEN)
                            game_info.full_screen = True
                        else:
                            game_info.screen = pygame.display.set_mode(
                                (game_info.width * 10, game_info.height * 10))
                            game_info.full_screen = False
                        draw_options()
                        pygame.display.update()
                    elif cur_pose == 1:
                        return main_menu()
                if event.key == pygame.K_ESCAPE:
                    return main_menu()
                if pygame.key.get_mods() & pygame.KMOD_ALT and \
                        event.key == pygame.K_F4:
                    pygame.quit()
                    sys.exit()


def main_menu():
    draw_menu()
    game_info = GameInfo()
    cur_pose = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    mx, my = pygame.mouse.get_pos()
                    if (game_info.width * 6 > mx > game_info.width * 4) and (
                            game_info.height * 4 > my > game_info.height * 3):
                        return main_loop()
                    elif (game_info.width * 6 > mx > game_info.width * 4) and (
                            game_info.height * 6 > my > game_info.height * 5):
                        return options()
                    elif (game_info.width * 6 > mx > game_info.width * 4) and (
                            game_info.height * 8 > my > game_info.height * 7):
                        pygame.quit()
                        sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_mods() & pygame.KMOD_ALT and \
                        event.key == pygame.K_F4:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN or \
                        event.key == pygame.K_KP_ENTER or \
                        event.key == pygame.K_SPACE:
                    if cur_pose == 0:
                        return main_loop()
                    elif cur_pose == 1:
                        return options()
                    elif cur_pose == 2:
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_DOWN:
                    if cur_pose < 2:
                        cur_pose += 1
                        draw_menu(cur_pose)
                elif event.key == pygame.K_UP:
                    if cur_pose > 0:
                        cur_pose -= 1
                        draw_menu(cur_pose)


if __name__ == '__main__':
    main_menu()
