import sys
from gameInfo import *
from button import Button


GRAY = (32, 32, 32)
GREEN = (0, 128, 0)
LIGHTGRAY = (128, 128, 128)
COOLCOLOR = (103, 153, 153)
RED = (128, 0, 0)


@singleton
class Options:
    def __init__(self):
        self.game_info = GameInfo()
        self.cur_pos = 0
        # fullscreen button
        fullscreen_button_rect = ((self.game_info.width * 4,
                                   self.game_info.height * 4,
                                   2 * self.game_info.width,
                                   self.game_info.height))
        self.fullscreen_button = Button('FULLSCREEN', COOLCOLOR,
                                        fullscreen_button_rect)

        # menu button
        menu_button_rect = (self.game_info.width * 4,
                            self.game_info.height * 6,
                            2 * self.game_info.width, self.game_info.height)
        self.menu_button = Button('BACK TO MENU', COOLCOLOR, menu_button_rect)

    def draw(self):
        self.game_info.screen.fill(GRAY)
        # fullscreen draw
        self.fullscreen_button.draw(self.game_info.screen)
        # menu button draw
        self.menu_button.draw(self.game_info.screen)

        self.game_info.screen.blit(
            pygame.transform.scale(self.game_info.arrow,
                                   (self.game_info.height,
                                    self.game_info.height)),
            (self.game_info.width * 3,
             int(self.game_info.height * (4 + 2 * self.cur_pos))))

        pygame.display.update()

    def toggle_fullscreen(self):
        if not self.game_info.full_screen:
            self.game_info.screen = pygame.display.set_mode(
                (self.game_info.window_width,
                 self.game_info.window_height),
                pygame.FULLSCREEN)
            self.game_info.full_screen = True
        else:
            self.game_info.screen = pygame.display.set_mode(
                (self.game_info.window_width,
                 self.game_info.window_height))
            self.game_info.full_screen = False

    def loop(self):
        self.draw()
        while True:
            for event in pygame.event.get():
                # mouse check
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0] == 1:
                        mouse_pt = pygame.mouse.get_pos()
                        if self.fullscreen_button.has(mouse_pt):
                            self.toggle_fullscreen()
                            self.draw()
                            pygame.display.update()
                        elif self.menu_button.has(mouse_pt):
                            return GameStatus.menu

                # check exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # keydown check
                if event.type == pygame.KEYDOWN:
                    # move arrow down
                    if event.key == pygame.K_DOWN:
                        if self.cur_pos < 1:
                            self.cur_pos += 1
                            self.draw()
                    # move arrow up
                    elif event.key == pygame.K_UP:
                        if self.cur_pos > 0:
                            self.cur_pos -= 1
                            self.draw()
                    # enter/space push the arrowed screen button
                    elif event.key == pygame.K_RETURN or \
                            event.key == pygame.K_KP_ENTER or \
                            event.key == pygame.K_SPACE:
                        if self.cur_pos == 0:
                            self.toggle_fullscreen()
                            self.draw()
                            pygame.display.update()
                        elif self.cur_pos == 1:
                            return GameStatus.menu
                    # return to main menu on escape
                    if event.key == pygame.K_ESCAPE:
                        return GameStatus.menu
                    # exit on alt+f4
                    if pygame.key.get_mods() & pygame.KMOD_ALT and \
                            event.key == pygame.K_F4:
                        pygame.quit()
                        sys.exit()


@singleton
class MainMenu:
    def __init__(self):
        self.game_info = GameInfo()
        self.cur_pos = 0
        # cat name rect
        cat_name_rect = (0, 0,
                         self.game_info.window_width, 3 * self.game_info.height)
        self.cat_name = Button(Cat().name, GRAY, cat_name_rect)

        # play button
        play_button_rect = (self.game_info.width * 4, self.game_info.height * 3,
                            2 * self.game_info.width, self.game_info.height)
        self.play_button = Button('START A GAME', GREEN, play_button_rect)

        # options button
        options_button_rect = (self.game_info.width * 4,
                               self.game_info.height * 5,
                               2 * self.game_info.width, self.game_info.height)
        self.options_button = Button('OPTIONS', COOLCOLOR, options_button_rect)

        # exit game button
        exit_button_rect = (self.game_info.width * 4, self.game_info.height * 7,
                            2 * self.game_info.width, self.game_info.height)
        self.exit_button = Button('EXIT', RED, exit_button_rect)

    def draw(self):
        self.game_info.screen.fill(GRAY)

        self.cat_name.draw(self.game_info.screen)
        self.play_button.draw(self.game_info.screen)
        self.options_button.draw(self.game_info.screen)
        self.exit_button.draw(self.game_info.screen)

        self.game_info.screen.blit(
            pygame.transform.scale(self.game_info.arrow,
                                   (self.game_info.height,
                                    self.game_info.height)),
            (self.game_info.width * 3, self.game_info.height *
             (3 + 2 * self.cur_pos)))

        pygame.display.update()

    def loop(self):
        self.draw()
        while True:
            for event in pygame.event.get():
                # mouse button click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0] == 1:
                        mouse_pt = pygame.mouse.get_pos()
                        if self.play_button.has(mouse_pt):
                            return GameStatus.loop
                        elif self.options_button.has(mouse_pt):
                            return GameStatus.options
                        elif self.exit_button.has(mouse_pt):
                            pygame.quit()
                            sys.exit()

                # exit check
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # keydown check
                if event.type == pygame.KEYDOWN:
                    # alt+f4 exit
                    if pygame.key.get_mods() & pygame.KMOD_ALT and \
                            event.key == pygame.K_F4:
                        pygame.quit()
                        sys.exit()
                    # enter/space push the arrowed screen button
                    elif event.key == pygame.K_RETURN or \
                            event.key == pygame.K_KP_ENTER or \
                            event.key == pygame.K_SPACE:
                        if self.cur_pos == 0:
                            return GameStatus.loop
                        elif self.cur_pos == 1:
                            return GameStatus.options
                        elif self.cur_pos == 2:
                            pygame.quit()
                            sys.exit()
                    # move down on down arrow
                    elif event.key == pygame.K_DOWN:
                        if self.cur_pos < 2:
                            self.cur_pos += 1
                            self.draw()
                    # move up on up arrow
                    elif event.key == pygame.K_UP:
                        if self.cur_pos > 0:
                            self.cur_pos -= 1
                            self.draw()
