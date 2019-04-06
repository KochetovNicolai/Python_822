import pygame
import menu
import field
import colours
import event_handler


gamefield = field.Field()

# ======== Инициализируем игровое окно  =============
pygame.init()
screen = pygame.display.set_mode(gamefield.field_size)
screen.fill(colours.BACKGROUND)
pygame.display.set_caption('Convey`s game of Life')
clock = pygame.time.Clock()
# ===================================================


# ==== Инициализируем меню, счетчик, режим игры =====
menu = menu.Menu(gamefield)
menu.draw(screen)

handler = event_handler.EventHandler()

done = False
mode = 'draw'  # В игре пять положения: draw, evolution, restart, quit, pause
# ===================================================


# ======== Основной цикл игры ===========
while not done:

    mode, done = handler.event_handler(pygame.event.get(), mode, done, gamefield, menu)

    # Обработка состояний игры
    if mode == 'draw' or mode == 'pause':
        gamefield.draw(screen)  # Отрисовка живых клеток
        clock.tick(30)

    elif mode == 'restart':
        screen.fill(colours.BACKGROUND)  # Обновление игрового поля
        gamefield.refresh()
        mode = 'draw'

    elif mode == 'evolution':
        gamefield.evolution_step()  # Один шаг эволюции
        gamefield.draw(screen)
        clock.tick(handler.evolution_tick)

    elif mode == 'gameover':
        gamefield.game_over(screen)  # Конец игры (При нажатии restart игра возобновится)

    if gamefield.is_dead:
        mode = 'gameover'  # Изменение состояния на gameover (по правилам игры)

    menu.draw(screen)

    pygame.display.flip()

pygame.quit()
