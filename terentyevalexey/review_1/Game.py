"""Игра про кота-качка. Кот хочет накачаться, помоги ему!
Коту нужно бить грушу, чтобы качать руки и ноги.
Так же коту нужно бегать, чтобы не перенапрягать мышцы,
а ещё ему необходимо отдыхать, чтобы не умереть.
"""


if __name__ == '__main__':
    from gameInfo import *
    from menu import MainMenu, Options
    from actions import *
    from handlers import *
    from drawSomething import draw_score

    caption = "Cat"
    logo = pygame.image.load(os.path.join('data', 'logo.png'))
    pygame.init()
    pygame.display.set_caption(caption)
    pygame.display.set_icon(logo)


def main_loop():
    cat = Cat()
    game_info = GameInfo()
    game_info.screen.blit(
        pygame.transform.scale(game_info.background, (game_info.window_width,
                                                      game_info.window_height)),
        (0, 0))
    clock = pygame.time.Clock()

    cat.status = Animations.idle
    cat.idle_time = 0
    pygame.time.set_timer(pygame.USEREVENT + 1, 6000)  # cat sleepy inc timer
    pygame.time.set_timer(pygame.USEREVENT + 2, 8000)  # cat muscle dec timer
    pygame.time.set_timer(pygame.USEREVENT + 3, 12000)  # cat cardio dec timer

    while True:
        # clock
        clock.tick(game_info.tick_rate)
        # screen update
        game_info.screen.blit(
            pygame.transform.scale(game_info.background, (
                game_info.window_width, game_info.window_height)), (0, 0))
        draw_score()
        cat.draw()

        # check cat's tiredness and drowsiness
        if cat.sleepy >= 20:
            Actions.sleep()
        if cat.tired > 10:
            return Actions.die()

        # event checker
        if events_handler() == GameStatus.menu:
            return GameStatus.menu

        # keys pressed checker
        keypress_handler()

        # idle checker
        idle_handler()

        # cat position checker
        cat_pos_handler()

        pygame.event.clear()


if __name__ == '__main__':
    cur_state = GameStatus.menu
    while cur_state is not None:
        if cur_state == GameStatus.menu:
            cur_state = MainMenu().loop()
        elif cur_state == GameStatus.options:
            cur_state = Options().loop()
        elif cur_state == GameStatus.loop:
            cur_state = main_loop()
        else:
            break
