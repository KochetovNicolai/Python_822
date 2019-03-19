import pygame
import scoreobj
import menu
import button
import field


gamefield = field.Field()

# ======== Инициализируем игровое окно  =============
pygame.init()
screen = pygame.display.set_mode(gamefield.field_size)
screen.fill(field.Field.BACKGROUND)
pygame.display.set_caption('Convey`s game of Life')
clock = pygame.time.Clock()
# ===================================================


# ==== Инициализируем меню, счетчик, режим игры =====
menu = menu.Menu(gamefield)
menu.draw(screen)

score = scoreobj.ScoreObj(  # Счётчик живых клеток
    (button.Button.widht + button.Button.margin) * 3,
    gamefield.field_size[1] - field.Field.menu_height
)

done = False
mode = 'draw'  # В игре четыре положения: draw, evolution, restart, quit
# ===================================================


# ======== Основной цикл игры ===========
while not done:
    # Обработка основных событий игры
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if mode == 'draw' and mouse_pos[1] < gamefield.field_size[1] - field.Field.menu_height:
                # print(mouse_pos)
                gamefield.click(mouse_pos)

            if mouse_pos[1] > gamefield.field_size[1] - field.Field.menu_height:
                mode = menu.click(mouse_pos, mode)
        if event.type == pygame.QUIT or mode == 'quit':
            done = True
        elif event.type == pygame.KEYDOWN and mode == 'draw':
            if event.key == pygame.K_RETURN:
                mode = 'evolution'  # начало эволюции
                print('evolution mode on')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    # Обработка состояний игры
    if mode == 'draw':
        gamefield.draw(screen)  # Отрисовка живых клеток
        clock.tick(30)

    elif mode == 'restart':
        screen.fill(field.Field.BACKGROUND)  # Обновление игрового поля
        gamefield.refresh()
        mode = 'draw'

    elif mode == 'evolution':
        gamefield.evolution_step()  # Один шаг эволюции
        gamefield.draw(screen)
        clock.tick(6)

    elif mode == 'gameover':
        gamefield.game_over(screen)  # Конец игры (При нажатии restart игра возобновится)

    if gamefield.is_dead:
        mode = 'gameover'  # Изменение состояния на gameover (по правилам игры)

    menu.draw(screen)
    score.draw(screen, gamefield)

    pygame.display.flip()

pygame.quit()
