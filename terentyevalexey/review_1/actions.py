import sys
import random
from gameInfo import *
from drawSomething import draw_score

GRAY = (32, 32, 32)


class Actions:
    cat = Cat()
    game_info = GameInfo()

    @classmethod
    def sleep(cls):
        cls.cat.status = Animations.sleep
        cls.cat.anim_time = 0
        clock = pygame.time.Clock()
        # this range used to make frames lasted the same time
        for _ in range(cls.game_info.tick_rate - cls.game_info.tick_rate % len(
                cls.cat.status.value)):
            clock.tick(cls.game_info.tick_rate)
            cls.game_info.screen.blit(
                pygame.transform.scale(cls.game_info.background, (
                    cls.game_info.window_width, cls.game_info.window_height)),
                (0, 0))
            draw_score()
            cls.cat.draw()
        for cur_time in range(10 * cls.game_info.tick_rate):
            clock.tick(cls.game_info.tick_rate)
            if cur_time % cls.game_info.tick_rate == 0:
                if cls.cat.sleepy > 0:
                    cls.cat.sleepy -= 1
                    if cur_time % (2 * cls.game_info.tick_rate) == 0 and \
                            cls.cat.tired > 0:
                        cls.cat.tired -= 1
                else:
                    return
            cls.game_info.screen.blit(
                pygame.transform.scale(cls.game_info.background, (
                    cls.game_info.window_width, cls.game_info.window_height)),
                (0, 0))
            draw_score()
            cls.game_info.screen.blit(
                pygame.transform.scale(Animations.sleep.value[6],
                                       (cls.game_info.width * 4,
                                        cls.game_info.height * 4)),
                (cls.cat.x, cls.cat.y))
            pygame.display.update()
            pygame.event.clear()

    @classmethod
    def run_cat_run(cls):
        cls.cat.status = Animations.walk
        cls.cat.anim_time = 0
        cls.cat.x = 0
        cls.cat.y = 6.7 * cls.game_info.height
        cur_x = 0
        clock = pygame.time.Clock()
        run_time = 200  # to complete full screen in reasonable time
        for _ in range(run_time):
            clock.tick(cls.game_info.tick_rate)
            bamboo_size = cls.game_info.bamboo.get_size()
            # rescale bamboo picture to fit the screen and move
            cls.game_info.screen.blit(pygame.transform.scale(
                cls.game_info.bamboo,
                (cls.game_info.window_height *
                 bamboo_size[0] // bamboo_size[1],
                 cls.game_info.window_height)),
                (0, 0), (cur_x, 0, cur_x +
                         bamboo_size[1] *
                         cls.game_info.width //
                         cls.game_info.height,
                         bamboo_size[1]))
            cls.cat.draw()
            cls.cat.x += cls.game_info.window_width // run_time
            cur_x += cls.game_info.window_width // run_time

        cls.game_info.screen.blit(pygame.transform.scale(
            cls.game_info.background, (cls.game_info.window_width,
                                       cls.game_info.window_height)), (0, 0))

        cls.cat.x = 4 * cls.game_info.width
        cls.cat.y = 5 * cls.game_info.height
        cls.cat.anim_time = 0
        cls.cat.idle_time = 0
        cls.cat.status = Animations.idle

        cls.cat.cardio += 2
        cls.cat.tired += 1

    @classmethod
    def hit_bag(cls):
        cls.cat.x = int(cls.game_info.width * 6.8)
        if random.randint(1, 2) == 1:
            cls.punching_bag()
        else:
            cls.kicking_bag()
        cls.cat.status = Animations.idle
        cls.cat.x = cls.game_info.width * 4
        cls.cat.anim_time = 0
        cls.cat.idle_time = 0

    @classmethod
    def punching_bag(cls):
        cls.cat.status = Animations.punch
        cls.cat.anim_time = 0
        clock = pygame.time.Clock()
        for _ in range(random.randint(2, 4) * cls.game_info.tick_rate):
            clock.tick(cls.game_info.tick_rate)
            cls.game_info.screen.blit(
                pygame.transform.scale(cls.game_info.background, (
                    cls.game_info.window_width, cls.game_info.window_height)),
                (0, 0))
            draw_score()
            cls.cat.draw()

        cls.cat.muscle += 3
        cls.cat.tired += 2

    @classmethod
    def kicking_bag(cls):
        cls.cat.status = Animations.kick
        cls.cat.anim_time = 0
        clock = pygame.time.Clock()
        for _ in range(random.randint(2, 4) * cls.game_info.tick_rate):
            clock.tick(cls.game_info.tick_rate)
            cls.game_info.screen.blit(
                pygame.transform.scale(cls.game_info.background,
                                       (
                                           cls.game_info.window_width,
                                           cls.game_info.window_height)),
                (0, 0))
            draw_score()
            cls.cat.draw()

        cls.cat.muscle += 2
        cls.cat.tired += 2

    @classmethod
    def die(cls):
        cls.cat.status = Animations.dead
        cls.cat.anim_time = 0
        clock = pygame.time.Clock()
        # this range used to make frames lasted the same time
        for _ in range(cls.game_info.tick_rate - cls.game_info.tick_rate % len(
                cls.cat.status.value)):
            clock.tick(cls.game_info.tick_rate)
            cls.game_info.screen.blit(
                pygame.transform.scale(cls.game_info.background, (
                    cls.game_info.window_width, cls.game_info.window_height)),
                (0, 0))
            draw_score()
            cls.cat.draw()

        font = pygame.font.SysFont("calibri", cls.game_info.height, True)
        text = font.render("{} is dead".format(cls.cat.name), True, GRAY)
        text_rect = text.get_rect()
        text_rect.center = (int(cls.game_info.width * 5.5),
                            cls.game_info.height * 9)
        cls.game_info.screen.blit(text, text_rect)

        font = pygame.font.SysFont("calibri", cls.game_info.height // 2, True)
        text = font.render("PRESS ANY KEY TO CONTINUE", True, GRAY)
        text_rect = text.get_rect()
        text_rect.center = (int(cls.game_info.width * 5.5),
                            int(cls.game_info.height * 9.7))
        cls.game_info.screen.blit(text, text_rect)

        pygame.display.update()

        cls.cat.reset()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return GameStatus.menu
