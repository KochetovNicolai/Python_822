import sys
from drawSomething import draw_menu, draw_options
from gameInfo import *


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
                        return GameStatus.menu

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
                        return GameStatus.menu
                if event.key == pygame.K_ESCAPE:
                    return GameStatus.menu
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
                        return GameStatus.loop
                    elif (game_info.width * 6 > mx > game_info.width * 4) and (
                            game_info.height * 6 > my > game_info.height * 5):
                        return GameStatus.options
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
                        return GameStatus.loop
                    elif cur_pose == 1:
                        return GameStatus.options
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
