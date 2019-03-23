"""
Тамагочи про кота-качка. Кот хочет накачаться, помоги ему!
Коту нужно бить грушу, чтобы качать руки и ноги.
Так же коту нужно бегать, чтобы не перенапрягать мышцы,
а ещё ему необходимо отдыхать и спать, чтобы не умереть.
"""

import random
import pygame
import sys
import os

logo = pygame.image.load(os.path.join('data', 'logo.png'))
background = pygame.image.load(os.path.join('data', 'background.jpg'))
arrow = pygame.image.load(os.path.join('data', 'arrow.png'))
bamboo = pygame.image.load(os.path.join('data', 'bamboo.jpg'))

pygame.init()
pygame.display.set_caption("cat")
pygame.display.set_icon(logo)
display_inf = pygame.display.Info()
width = display_inf.current_w // 20
height = display_inf.current_h // 20
full_screen = False
screen = pygame.display.set_mode((width * 10, height * 10))

tick_rate = 30


class Cat:
    name = "Kitty"
    x = width * 4
    y = height * 5
    anim_time = 0
    idle_time = 0

    cardio = 0
    muscle = 0
    tired = 0
    sleepy = 0

    animations = {
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


def cat_reset():
    Cat.name = "Kitty"
    Cat.x = width * 4
    Cat.y = height * 5
    Cat.anim_time = 0
    Cat.idle_time = 0
    Cat.cardio = 0
    Cat.muscle = 0
    Cat.tired = 0
    Cat.sleepy = 0


def sleep():
    Cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(tick_rate // 7 * 7):
        clock.tick(tick_rate)
        screen.blit(
            pygame.transform.scale(background, (width * 10, height * 10)),
            (0, 0))
        draw_score()
        draw_cat("sleep")
    for cur_time in range(10 * tick_rate):
        clock.tick(tick_rate)
        if cur_time % tick_rate == 0:
            if Cat.sleepy > 0:
                Cat.sleepy -= 1
                if cur_time % (2 * tick_rate) == 0 and Cat.tired > 0:
                    Cat.tired -= 1
            else:
                return
        screen.blit(
            pygame.transform.scale(background, (width * 10, height * 10)),
            (0, 0))
        draw_score()
        screen.blit(pygame.transform.scale(Cat.animations["sleep"][6],
                                           (width * 4, height * 4)),
                    (Cat.x, Cat.y))
        pygame.display.update()
        pygame.event.clear()


def run_cat_run():
    Cat.anim_time = 0
    Cat.x = 0
    Cat.y = 6.7 * height
    cur_x = 0
    clock = pygame.time.Clock()
    for _ in range(200):
        clock.tick(tick_rate)
        screen.blit(pygame.transform.scale(bamboo, (height * 48, height * 10)),
                    (0, 0), (cur_x, 0, cur_x + 2133, 1200))
        draw_cat("walk")
        Cat.x += width // 20
        cur_x += width // 20

    screen.blit(pygame.transform.scale(background, (width * 10, height * 10)),
                (0, 0))

    Cat.x = 4 * width
    Cat.y = 5 * height
    Cat.anim_time = 0

    Cat.cardio += 2
    Cat.tired += 1


def punching_bag():
    Cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(random.randint(2, 4) * tick_rate):
        clock.tick(tick_rate)
        screen.blit(
            pygame.transform.scale(background, (width * 10, height * 10)),
            (0, 0))
        draw_score()
        draw_cat("punch")

    Cat.muscle += 3
    Cat.tired += 2


def kicking_bag():
    Cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(random.randint(2, 4) * tick_rate):
        clock.tick(tick_rate)
        screen.blit(
            pygame.transform.scale(background, (width * 10, height * 10)),
            (0, 0))
        draw_score()
        draw_cat("kick")

    Cat.muscle += 2
    Cat.tired += 2


def die():
    Cat.anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(tick_rate // 7 * 7):
        clock.tick(tick_rate)
        screen.blit(
            pygame.transform.scale(background, (width * 10, height * 10)),
            (0, 0))
        draw_score()
        draw_cat("dead")

    font = pygame.font.SysFont("calibri", height, bold=True)
    text = font.render("{} is dead".format(Cat.name), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (width * 5.5, height * 9)
    screen.blit(text, text_rect)

    font = pygame.font.SysFont("calibri", height // 2, bold=True)
    text = font.render("PRESS ANY KEY TO CONTINUE", True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (width * 5.5, height * 9.7)
    screen.blit(text, text_rect)

    pygame.display.update()

    cat_reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return main_menu()


def draw_cat(status):
    if Cat.anim_time >= tick_rate:
        Cat.anim_time = 0

    cur_frame = Cat.anim_time // (
            tick_rate //
            len(Cat.animations[status]))
    Cat.anim_time += 1
    if cur_frame >= len(Cat.animations[status]):
        Cat.anim_time = 0
        return
    screen.blit(pygame.transform.scale(Cat.animations[status][cur_frame],
                                       (width * 4, height * 4)),
                (Cat.x, Cat.y))
    pygame.display.update()


def draw_score():
    font = pygame.font.SysFont("calibri", height // 2, bold=True)

    text = font.render(str(Cat.tired), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (width * 4, height * 4.35)
    screen.blit(text, text_rect)

    text = font.render(str(Cat.muscle), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (width * 5, height * 4.05)
    screen.blit(text, text_rect)

    text = font.render(str(Cat.cardio), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (width * 5.975, height * 4.35)
    screen.blit(text, text_rect)

    text = font.render(str(Cat.sleepy), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (width * 6.975, height * 4.05)
    screen.blit(text, text_rect)


def main():
    screen.blit(pygame.transform.scale(background, (width * 10, height * 10)),
                (0, 0))
    clock = pygame.time.Clock()

    status = "idle"
    Cat.idle_time = 0
    pygame.time.set_timer(pygame.USEREVENT + 1, 6000)  # cat sleepy inc
    pygame.time.set_timer(pygame.USEREVENT + 2, 8000)  # cat muscle dec
    pygame.time.set_timer(pygame.USEREVENT + 3, 12000)  # cat cardio dec

    while True:
        clock.tick(tick_rate)

        if Cat.muscle > 30:
            Cat.muscle -= 1
        if Cat.cardio > 30:
            Cat.cardio -= 1

        screen.blit(
            pygame.transform.scale(background, (width * 10, height * 10)),
            (0, 0))
        draw_score()
        draw_cat(status)

        if Cat.sleepy >= 20:
            sleep()
        if Cat.tired > 10:
            return die()

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                Cat.sleepy += 1
            if event.type == pygame.USEREVENT + 2:
                if Cat.muscle > 0:
                    Cat.muscle -= 1
            if event.type == pygame.USEREVENT + 3:
                if Cat.cardio > 0:
                    Cat.cardio -= 1

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
                    Cat.x = width * 6.8
                    if random.randint(1, 2) == 1:
                        punching_bag()
                    else:
                        kicking_bag()
                    status = "idle"
                    Cat.x = width * 4
                    Cat.anim_time = 0
                    Cat.idle_time = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    mx, my = pygame.mouse.get_pos()
                    if (mx > width * 9) and (
                            height * 6 < my < height * 9.5):
                        Cat.x = width * 6.8
                        if random.randint(1, 2) == 1:
                            punching_bag()
                        else:
                            kicking_bag()
                        status = "idle"
                        Cat.x = width * 4
                        Cat.anim_time = 0
                        Cat.idle_time = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if status != "walk":
                Cat.anim_time = 0
                status = "walk"
            Cat.x += width // 10

        elif keys[pygame.K_LEFT]:
            if status != "walk_left":
                Cat.anim_time = 0
                status = "walk_left"
            Cat.x -= width // 10

        elif status != "idle":
            status = "idle"
            Cat.anim_time = 0
            Cat.idle_time = 0

        if status == "idle":
            Cat.idle_time += 1
            if Cat.idle_time == tick_rate * 5 and Cat.tired > 0:
                Cat.tired -= 1
                Cat.idle_time = 0

        if Cat.x >= width * 6.8:
            Cat.x = width * 6.8
            if random.randint(1, 2) == 1:
                punching_bag()
            else:
                kicking_bag()
            status = "idle"
            Cat.x = width * 4
            Cat.anim_time = 0
            Cat.idle_time = 0

        if Cat.x <= - 2 * width:
            run_cat_run()
            status = "idle"
            Cat.x = width * 4
            Cat.anim_time = 0
            Cat.idle_time = 0

        pygame.event.clear()


def draw_menu(pos=0):
    screen.fill((32, 32, 32))
    # draw game name
    font = pygame.font.SysFont("calibri", height, bold=True)
    text = font.render(Cat.name, True, (100, 100, 100))
    text_rect = text.get_rect()
    text_rect.center = (width * 5, height * 1.5)
    screen.blit(text, text_rect)

    font = pygame.font.SysFont("calibri", height // 2, bold=True)

    # play draw
    pygame.draw.rect(screen, (0, 128, 0),
                     (width * 4, height * 3, 2 * width, height))
    text = font.render("START A GAME", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width * 5, height * 3.55)
    screen.blit(text, text_rect)

    # options draw
    pygame.draw.rect(screen, (102, 153, 153),
                     (width * 4, height * 5, 2 * width, height))
    text = font.render("OPTIONS", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width * 5, height * 5.55)
    screen.blit(text, text_rect)

    # exit game draw
    pygame.draw.rect(screen, (128, 0, 0),
                     (width * 4, height * 7, 2 * width, height))
    text = font.render("EXIT", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width * 5, height * 7.55)
    screen.blit(text, text_rect)

    screen.blit(pygame.transform.scale(arrow, (height, height)),
                (width * 3.3, height * (3 + 2 * pos)))

    pygame.display.update()


def draw_options(pos=0):
    screen.fill((32, 32, 32))
    font = pygame.font.SysFont("calibri", height // 2, bold=True)

    # fullscreen draw
    pygame.draw.rect(screen, (102, 153, 153),
                     (width * 4, height * 3.5, 2 * width, height))
    text = font.render("FULLSCREEN", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width * 5, height * 4.05)
    screen.blit(text, text_rect)

    # menu button draw
    pygame.draw.rect(screen, (102, 153, 153),
                     (width * 4, height * 5.5, 2 * width, height))
    text = font.render("BACK TO MENU", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width * 5, height * 6.05)
    screen.blit(text, text_rect)

    screen.blit(pygame.transform.scale(arrow, (height, height)),
                (width * 3.3, height * (3.5 + 2 * pos)))

    pygame.display.update()


def options():
    cur_pose = 0
    draw_options()
    global screen, full_screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    mx, my = pygame.mouse.get_pos()
                    if (width * 6 > mx > width * 4) and (
                            height * 4.5 > my > height * 3.5):
                        if not full_screen:
                            screen = pygame.display.set_mode(
                                (width * 10, height * 10), pygame.FULLSCREEN)
                            full_screen = True
                        else:
                            screen = pygame.display.set_mode(
                                (width * 10, height * 10))
                            full_screen = False
                        draw_options()
                        pygame.display.update()
                    elif (width * 6 > mx > width * 4) and (
                            height * 6.5 > my > height * 5.5):
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
                        if not full_screen:
                            screen = pygame.display.set_mode(
                                (width * 10, height * 10), pygame.FULLSCREEN)
                            full_screen = True
                        else:
                            screen = pygame.display.set_mode(
                                (width * 10, height * 10))
                            full_screen = False
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
    cur_pose = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    mx, my = pygame.mouse.get_pos()
                    if (width * 6 > mx > width * 4) and (
                            height * 4 > my > height * 3):
                        return main()
                    elif (width * 6 > mx > width * 4) and (
                            height * 6 > my > height * 5):
                        return options()
                    elif (width * 6 > mx > width * 4) and (
                            height * 8 > my > height * 7):
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
                        return main()
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


main_menu()
