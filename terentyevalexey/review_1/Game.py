"""Игра про кота-качка. Кот хочет накачаться, помоги ему!
Коту нужно бить грушу, чтобы качать руки и ноги.
Так же коту нужно бегать, чтобы не перенапрягать мышцы,
а ещё ему необходимо отдыхать, чтобы не умереть.
"""

import random
import pygame
import sys
import os

Full_screen = False
Game_name = "Game"
pygame.init()
pygame.display.set_caption(Game_name)
display_inf = pygame.display.Info()
width = display_inf.current_w // 20
height = display_inf.current_h // 20
screen = pygame.display.set_mode((width * 10, height * 10))
cat = pygame.image.load(os.path.join('data', 'cat.png'))
background = pygame.image.load(os.path.join('data', 'background.jpg'))
arrow = pygame.image.load(os.path.join('data', 'arrow.png'))
bamboo = pygame.image.load(os.path.join('data', 'bamboo.jpg'))

tick_rate = 30
anim_time = 0

cat_x, cat_y = width * 4, height * 5
cat_cardio, cat_muscle, cat_tired = 0, 0, 0

animations = {
    "idle": [
        pygame.image.load(os.path.join('data', 'cat', 'idle_{}.png'.format(i)))
        for i in range(1, 5)],
    "dead": [
        pygame.image.load(os.path.join('data', 'cat', 'dead_{}.png'.format(i)))
        for i in range(1, 8)],
    "kick": [
        pygame.image.load(os.path.join('data', 'cat', 'kick_{}.png'.format(i)))
        for i in range(1, 9)],
    "punch": [
        pygame.image.load(os.path.join('data', 'cat', 'punch_{}.png'.format(i)))
        for i in range(1, 7)],
    "walk": [
        pygame.image.load(os.path.join('data', 'cat', 'walk_{}.png'.format(i)))
        for i in range(1, 9)],
    "walk_left": [
        pygame.image.load(
            os.path.join('data', 'cat', 'walk_left_{}.png'.format(i)))
        for i in range(1, 9)]
}


def run_cat_run():
    global cat_x, cat_y, cat_cardio, cat_tired, anim_time
    anim_time = 0
    cat_x = 0
    cat_y = 6.7 * height
    cur_x = 0
    clock = pygame.time.Clock()
    for _ in range(153):
        clock.tick(tick_rate)
        screen.blit(pygame.transform.scale(bamboo, (height * 48, height * 10)),
                    (0, 0), (cur_x, 0, cur_x + 2133, 1200))
        draw_cat("walk")
        cat_x += 5
        cur_x += 5

    screen.blit(pygame.transform.scale(background, (width * 10, height * 10)),
                (0, 0))
    cat_x = 4 * width
    cat_y = 5 * height
    anim_time = 0
    cat_cardio += 2
    cat_tired += 1


def punching_bag():
    global anim_time, cat_muscle, cat_tired
    anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(random.randint(10, 15) * 7):
        clock.tick(tick_rate)
        screen.blit(
            pygame.transform.scale(background, (width * 10, height * 10)),
            (0, 0))
        draw_score()
        draw_cat("punch")
    cat_muscle += 3
    cat_tired += 2


def kicking_bag():
    global anim_time, cat_muscle, cat_tired
    anim_time = 0
    clock = pygame.time.Clock()
    for _ in range(random.randint(10, 15) * 9):
        clock.tick(tick_rate)
        screen.blit(
            pygame.transform.scale(background, (width * 10, height * 10)),
            (0, 0))
        draw_score()
        draw_cat("kick")
    cat_muscle += 2
    cat_tired += 2


def draw_cat(status):
    global anim_time

    anim_time += 1
    if anim_time >= tick_rate:
        anim_time = 0

    cur_frame = anim_time // (
            (tick_rate - tick_rate % len(animations[status])) //
            len(animations[status])) + 1
    if cur_frame >= len(animations[status]):
        anim_time = 0
        return
    screen.blit(pygame.transform.scale(animations[status][cur_frame],
                                       (width * 4, height * 4)),
                (cat_x, cat_y))
    pygame.display.update()


def draw_score():
    font = pygame.font.SysFont("calibri", height // 2, bold=True)

    text = font.render(str(cat_tired), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (width * 4, height * 4.35)
    screen.blit(text, text_rect)

    text = font.render(str(cat_muscle), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (width * 5, height * 4.05)
    screen.blit(text, text_rect)

    text = font.render(str(cat_cardio), True, (32, 32, 32))
    text_rect = text.get_rect()
    text_rect.center = (width * 6, height * 4.35)
    screen.blit(text, text_rect)


def main():
    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(background, (width * 10, height * 10)),
                (0, 0))
    clock = pygame.time.Clock()

    global anim_time, cat_x, cat_y, cat_tired, cat_muscle, cat_cardio
    status = "idle"

    while True:
        clock.tick(tick_rate)

        screen.blit(
            pygame.transform.scale(background, (width * 10, height * 10)),
            (0, 0))
        draw_score()
        draw_cat(status)

        pygame.time.get_ticks()

        if cat_muscle > 30:
            cat_muscle -= 1
        if cat_cardio > 30:
            cat_cardio -= 1
        if cat_tired > 20:
            die()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif pygame.key.get_mods() & pygame.KMOD_ALT and \
                        event.key == pygame.K_F4:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN or \
                        event.key == pygame.K_KP_ENTER:
                    run_cat_run()

                elif event.key == pygame.K_SPACE:
                    cat_x = width * 6.8
                    if random.randint(1, 2) == 1:
                        punching_bag()
                    else:
                        kicking_bag()
                    status = "idle"
                    cat_x = width * 4
                    anim_time = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    mx, my = pygame.mouse.get_pos()
                    if (mx > width * 9) and (
                            height * 6 < my < height * 9.5):
                        cat_x = width * 6.8
                        if random.randint(1, 2) == 1:
                            punching_bag()
                        else:
                            kicking_bag()
                        status = "idle"
                        cat_x = width * 4
                        anim_time = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if status != "walk":
                anim_time = 0
                status = "walk"
            cat_x += 10

        elif keys[pygame.K_LEFT]:
            if status != "walk_left":
                anim_time = 0
                status = "walk_left"
            cat_x -= 10

        elif status != "idle":
            status = "idle"
            anim_time = 0

        if cat_x >= width * 6.8:
            cat_x = width * 6.8
            if random.randint(1, 2) == 1:
                punching_bag()
            else:
                kicking_bag()
            status = "idle"
            cat_x = width * 4
            anim_time = 0

        if cat_x <= - 2 * width:
            run_cat_run()
            status = "idle"
            cat_x = width * 4
            anim_time = 0


# draws main menu
def draw_menu(pos=0):
    screen.fill((32, 32, 32))
    # draw game name
    font = pygame.font.SysFont("calibri", height, bold=True)
    text = font.render(Game_name, True, (100, 100, 100))
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
    global screen, Full_screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    mx, my = pygame.mouse.get_pos()
                    if (width * 6 > mx > width * 4) and (
                            height * 4.5 > my > height * 3.5):
                        if not Full_screen:
                            screen = pygame.display.set_mode(
                                (width * 10, height * 10), pygame.FULLSCREEN)
                            Full_screen = True
                        else:
                            screen = pygame.display.set_mode(
                                (width * 10, height * 10))
                            Full_screen = False
                        draw_options()
                        pygame.display.update()
                    elif (width * 6 > mx > width * 4) and (
                            height * 6.5 > my > height * 5.5):
                        return

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
                        if not Full_screen:
                            screen = pygame.display.set_mode(
                                (width * 10, height * 10), pygame.FULLSCREEN)
                            Full_screen = True
                        else:
                            screen = pygame.display.set_mode(
                                (width * 10, height * 10))
                            Full_screen = False
                        draw_options()
                        pygame.display.update()
                    elif cur_pose == 1:
                        return
                if event.key == pygame.K_ESCAPE:
                    return
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
                        main()
                        cur_pose = 0
                        draw_menu()
                        continue
                    elif (width * 6 > mx > width * 4) and (
                            height * 6 > my > height * 5):
                        options()
                        cur_pose = 0
                        draw_menu()
                        continue
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
                        main()
                        draw_menu()
                        continue
                    elif cur_pose == 1:
                        options()
                        cur_pose = 0
                        draw_menu()
                        continue
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
