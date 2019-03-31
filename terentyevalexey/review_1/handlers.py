from actions import *
import pygame


def keydown_handler(event):
    # return to menu on esc
    if event.key == pygame.K_ESCAPE:
        return 0
    # quit on alt+f4
    elif pygame.key.get_mods() & pygame.KMOD_ALT and \
            event.key == pygame.K_F4:
        pygame.quit()
        sys.exit()
    # run on enter
    elif event.key == pygame.K_RETURN or \
            event.key == pygame.K_KP_ENTER:
        run_cat_run()
    # hit bag on space
    elif event.key == pygame.K_SPACE:
        hit_bag()


def mouse_click_handler():
    game_info = GameInfo()
    # hit bag when click it
    if pygame.mouse.get_pressed()[0] == 1:
        mx, my = pygame.mouse.get_pos()
        if (mx > game_info.width * 9) and (
                game_info.height * 6 < my < game_info.height * 9.5):
            hit_bag()


def events_handler():
    cat = Cat()
    for event in pygame.event.get():
        # stats updater by event
        cat.update_stats(event)

        # exit checker
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # keydown checker for events
        if event.type == pygame.KEYDOWN:
            keydown_handler(event)

        # mouse click checker for events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click_handler()


def keypress_handler():
    cat = Cat()
    game_info = GameInfo()
    # get keys to move cat
    keys = pygame.key.get_pressed()

    # walk right when right keydown, has prior to left keydown
    if keys[pygame.K_RIGHT]:
        if cat.status != Animations.walk:
            cat.anim_time = 0
            cat.status = Animations.walk
        cat.x += game_info.width // 10

    # walk left when left keydown
    elif keys[pygame.K_LEFT]:
        if cat.status != Animations.walk_left:
            cat.anim_time = 0
            cat.status = Animations.walk_left
        cat.x -= game_info.width // 10

    # become idle, all events passed, neither of L/R keys pressed
    elif cat.status != Animations.idle:
        cat.status = Animations.idle
        cat.anim_time = 0
        cat.idle_time = 0


def idle_handler():
    cat = Cat()
    game_info = GameInfo()
    if cat.status == Animations.idle:
        cat.idle_time += 1
        # every 5 seconds cat rests for 1 tiredness point
        if cat.idle_time == game_info.tick_rate * 5 and cat.tired > 0:
            cat.tired -= 1
            cat.idle_time = 0


def cat_pos_handler():
    cat = Cat()
    game_info = GameInfo()
    # if cat walks to bag, he hits it
    if cat.x >= game_info.width * 6.8:
        hit_bag()

    # if cat walks to the left border he starts running
    if cat.x <= - 2 * game_info.width:
        run_cat_run()
